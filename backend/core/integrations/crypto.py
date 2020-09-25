from typing import Tuple, List
import ujson
from os import path

from bson import Decimal128
from datetime import datetime
from web3 import Web3
from web3.middleware import geth_poa_middleware
from passlib import pwd
from decimal import Decimal
from fastapi import HTTPException
from http import HTTPStatus
from sentry_sdk import capture_message

from schemas.user import User
from core.utils.gas_station import gas_price_from_ethgasstation
from database.crud.transaction import USDTTransactionCRUD
from schemas.transaction import USDTTransaction, USDTTransactionStatus, USDTTransactionEvents
from schemas.notification import Notification, NotificationType
from database.crud.notification import NotificationCRUD
from config import (
    BASE_DIR,
    INFURA_URL_TESTNET,
    INFURA_URL_MAINNET,
    IS_PRODUCTION,
    ABI_FILEPATH_MAINNET,
    ABI_FILEPATH_TESTNET,
    USDT_CONTRACT_ADDRESS_MAINNET,
    USDT_CONTRACT_ADDRESS_TESTNET,
    HOT_WALLET_ADDRESS_MAINNET,
    HOT_WALLET_ADDRESS_TESTNET,
    HOT_WALLET_PRIVATE_KEY_MAINNET,
    HOT_WALLET_PRIVATE_KEY_TESTNET
)


GAS = 90000


class USDTWrapper:
    def __init__(self):
        self.hot_wallet_addr = Web3.toChecksumAddress(
            HOT_WALLET_ADDRESS_MAINNET.lower() if IS_PRODUCTION else HOT_WALLET_ADDRESS_TESTNET.lower()
        )
        self.hot_wallet_private_key = (
            HOT_WALLET_PRIVATE_KEY_MAINNET.lower() if IS_PRODUCTION else HOT_WALLET_PRIVATE_KEY_TESTNET.lower()
        )
        self.w3 = Web3(Web3.WebsocketProvider(INFURA_URL_MAINNET if IS_PRODUCTION else INFURA_URL_TESTNET))
        self._abi = []
        self.contract_address = Web3.toChecksumAddress(
            USDT_CONTRACT_ADDRESS_MAINNET.lower() if IS_PRODUCTION else USDT_CONTRACT_ADDRESS_TESTNET.lower()
        )
        with open(path.join(
                BASE_DIR,
                "config",
                ABI_FILEPATH_MAINNET if IS_PRODUCTION else ABI_FILEPATH_TESTNET)
        ) as f:
            self._abi = ujson.load(f)
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self._abi)
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    async def create_wallet(self) -> Tuple[str, str, str]:
        entropy = pwd.genword()
        account = self.w3.eth.account.create(entropy)

        return (
            account.address,
            account.privateKey.hex(),
            entropy
        )

    @staticmethod
    async def _approve_withdraw(tx_hash: str, amount: Decimal) -> None:
        tx = await USDTTransactionCRUD.find_one(
            query={
                "tx_hash": tx_hash
            }
        )
        new_notification = Notification(
            type=NotificationType.WITHDRAW,
            watched=False,
            user_id=tx.get("user_id"),
            created_at=datetime.utcnow(),
            amount=float(float(amount) * 0.000001)
        )
        await NotificationCRUD.create_notification(new_notification)

    async def parse_last_blocks(self, last_blocks: int) -> List[dict]:
        last_block_number: int = self.w3.eth.getBlock("latest").get("number")
        tx_hashes = set()
        pending_tx = await USDTTransactionCRUD.find_many(
            query={"status": USDTTransactionStatus.PENDING}
        )
        set_of_pending_tx_hashes = set()
        for trans in pending_tx:
            set_of_pending_tx_hashes.add(trans.get("tx_hash"))

        transactions_in_db = await USDTTransactionCRUD.find_many({"status": USDTTransactionStatus.DONE})
        for i in transactions_in_db:
            tx_hashes.add(i.get("tx_hash"))
        transactions_to_proceed = []
        for block_number in range(last_block_number, last_block_number - last_blocks - 1, -1):
            transactions = self.w3.eth.getBlock(block_number, full_transactions=True).get("transactions")
            for transaction in transactions:
                try:

                    if not transaction.get("to") or transaction.get("to").lower() != self.contract_address.lower():
                        continue
                    input_field = self.contract.decode_function_input(transaction.get("input"))

                    if transaction.get("hash").hex() in set_of_pending_tx_hashes:
                        await USDTTransactionCRUD.approve_withdraw(transaction.get("hash").hex())
                        await self._approve_withdraw(
                            transaction.get("hash").hex(),
                            Decimal(input_field[1].get("_value"))
                        )

                    if (
                            len(input_field) >= 2 and
                            "_to" in input_field[1] and
                            transaction.get("hash").hex() not in tx_hashes
                    ):
                        parsed_trans = {
                            "to_adr": input_field[1].get("_to"),
                            "from_adr": transaction.get("from"),
                            "tx_hash": transaction.get("hash").hex(),
                            "usdt_amount": Decimal(input_field[1].get("_value"))
                        }
                        transactions_to_proceed.append(parsed_trans)
                except ValueError:
                    pass

        return transactions_to_proceed

    def _get_nonce(self):
        return self.w3.eth.getTransactionCount(self.hot_wallet_addr, "pending")

    @staticmethod
    async def get_gas_price():
        actual_gas_price_gwei = await gas_price_from_ethgasstation()
        return Web3.toWei(actual_gas_price_gwei, "gwei")

    async def _get_balance(self, adr: str) -> float:
        return self.contract.functions.balanceOf(adr).call()

    async def withdraw(self, user: User, to: str, value: Decimal) -> bool:
        to = self.w3.toChecksumAddress(to.lower())
        if not self.w3.isAddress(to):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong address")
        balance = await self._get_balance(self.hot_wallet_addr)
        if balance < value:
            capture_message("No usdt on hot wallet")
            raise HTTPException(HTTPStatus.BAD_REQUEST, "No usdt on hot wallet")
        tx = self.contract.functions.transfer(to, int(value)).buildTransaction({
            "from": self.hot_wallet_addr,
            "nonce": self._get_nonce(),
            "gas": GAS,
            "gasPrice": await self.get_gas_price(),
        })
        signed_txn = self.w3.eth.account.signTransaction(tx, private_key=self.hot_wallet_private_key)
        tx_hash = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
        new_trans = USDTTransaction(
            date=datetime.utcnow(),
            to_adr=to,
            from_adr=self.hot_wallet_addr,
            tx_hash=tx_hash,
            event=USDTTransactionEvents.WITHDRAW,
            status=USDTTransactionStatus.PENDING,
            usdt_amount=Decimal128(value),
            user_id=user.id
        )
        dct = new_trans.dict()
        dct["usdt_amount"] = Decimal128(dct["usdt_amount"])
        await USDTTransactionCRUD.insert_one(dct)
        return True
