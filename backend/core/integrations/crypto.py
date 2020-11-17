import ujson
import time
from typing import Tuple, List
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
from database.crud.transaction import USDTTransactionCRUD
from database.crud.ethereum_wallet import EthereumWalletCRUD
from schemas.transaction import USDTTransaction, USDTTransactionStatus, USDTTransactionEvents
from core.utils.etherscan_gas_tracker_wrapper import gasprice_from_etherscan
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
    HOT_WALLET_PRIVATE_KEY_TESTNET,
    ETH_MAX_GAS_PRICE_GWEI,
    ETH_MAX_GAS,
    ETH_MAX_GAS_DEPOSIT_LOOT,
    ETH_MAX_GAS_ETH_SEND
)


class USDTWrapper:
    gasprice_wrapper = gasprice_from_etherscan

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
                    try:
                        if not transaction.get("to") or transaction.get("to").lower() != self.contract_address.lower():
                            continue
                    except AttributeError:
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

    def _get_nonce_deposits(self, adr: str):
        return self.w3.eth.getTransactionCount(adr, "pending")

    @classmethod
    async def get_actual_gasprice(cls) -> int:
        gasprice = await cls.gasprice_wrapper()
        return Web3.toWei(min(int(gasprice), ETH_MAX_GAS_PRICE_GWEI), "gwei")

    async def get_hot_wallet_balance(self) -> int:
        return Decimal(str(self.contract.functions.balanceOf(self.hot_wallet_addr).call()))

    async def _get_balance_contract(self, adr: str) -> int:
        return self.contract.functions.balanceOf(adr).call()

    async def _get_eth_balance(self, adr: str) -> int:
        return self.w3.eth.getBalance(account=adr)

    async def get_balance_contract(self, adr: str) -> int:
        address = self.w3.toChecksumAddress(adr)
        return self.contract.functions.balanceOf(address).call()

    async def get_eth_balance(self, adr: str) -> int:
        address = self.w3.toChecksumAddress(adr)
        return self.w3.eth.getBalance(account=address)

    async def transfer_from_deposits(self, addresses: List[dict]) -> List[dict]:
        """
        Take all addresses which have some money to send and make a transaction to the hot wallet.
        Returns addresses which have not negative balance but don't have enough gas.
        :param addresses:
        :return: None
        """
        parsed_addresses = []
        for address in addresses:
            if self.w3.isAddress(self.w3.toChecksumAddress(address.get("eth_address").lower())):
                address["eth_address"] = self.w3.toChecksumAddress(address.get("eth_address").lower())
                parsed_addresses.append(address)
        not_enough_gas_addresses = []
        for address in parsed_addresses:
            eth_balance = await self._get_eth_balance(address.get("eth_address"))
            if eth_balance < (await self.get_actual_gasprice()) * ETH_MAX_GAS_DEPOSIT_LOOT:
                not_enough_gas_addresses.append(address)
            else:
                contract_balance = await self._get_balance_contract(address.get("eth_address"))
                if contract_balance >= 5 * 10**6:
                    tx = self.contract.functions.transfer(self.hot_wallet_addr, contract_balance).buildTransaction({
                        "from": address.get("eth_address"),
                        "nonce": self._get_nonce_deposits(address.get("eth_address")),
                        "gas": ETH_MAX_GAS_DEPOSIT_LOOT,
                        "gasPrice": await self.get_actual_gasprice(),
                    })
                    try:
                        signed_txn = self.w3.eth.account.signTransaction(tx, private_key=address.get("private_key"))
                        tx_hash = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
                        # Sending tx to blockchain
                    except ValueError as e:
                        print(f"Error while pushing deposit transaction {e}")
                        continue

                    await EthereumWalletCRUD.update_one(
                        query={"eth_address": str(address.get("eth_address")).lower()},
                        payload={"contract_balance": Decimal128(str(0))}
                    )
                    new_tx = USDTTransaction(
                        event=USDTTransactionEvents.DEPOSIT_LOOT_TOKENS,
                        date=datetime.utcnow(),
                        to_adr=self.hot_wallet_addr,
                        from_adr=address.get("eth_address"),
                        tx_hash=tx_hash,
                        status=USDTTransactionStatus.DONE,
                        usdt_amount=Decimal128(str(contract_balance))
                    )
                    new_tx.usdt_amount = Decimal128(new_tx.usdt_amount)
                    await USDTTransactionCRUD.insert_one(payload=new_tx.dict())
                    print(f"New transaction! {tx_hash}")
        return not_enough_gas_addresses

    async def send_gas_to_addresses(self, addresses: List[dict]) -> None:
        """
        Takes addresses and send 2.5-3$ to them
        :param addresses:
        :return:
        """
        value = await self.get_actual_gasprice() * ETH_MAX_GAS_ETH_SEND
        balance = await self._get_eth_balance(self.hot_wallet_addr)
        for address in addresses:
            if balance < value:
                capture_message("No ether on hot wallet")
                return
            actual_gasprice = await self.get_actual_gasprice()
            balance -= (7000000000000000 + ETH_MAX_GAS_DEPOSIT_LOOT * actual_gasprice)
            signed_txn = self.w3.eth.account.signTransaction(
                {
                    "from": self.hot_wallet_addr,
                    "to": address.get("eth_address"),
                    "value": 7000000000000000,
                    "nonce": self._get_nonce(),
                    "gas": ETH_MAX_GAS_DEPOSIT_LOOT,
                    "gasPrice": actual_gasprice,
                },
                private_key=self.hot_wallet_private_key
            )
            tx_hash = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
            new_tx = USDTTransaction(
                event=USDTTransactionEvents.DEPOSIT_LOOT_ETHER,
                date=datetime.utcnow(),
                to_adr=address.get("eth_address"),
                from_adr=self.hot_wallet_addr,
                tx_hash=tx_hash,
                status=USDTTransactionStatus.DONE,
                ether_amount=Decimal128(str(value)),
            )
            new_tx.ether_amount = Decimal128(new_tx.ether_amount)
            await USDTTransactionCRUD.insert_one(payload=new_tx.dict())
            print(f"New trasnaction! {tx_hash}")

    async def withdraw(self, user: User, to: str, value: Decimal) -> bool:
        to = self.w3.toChecksumAddress(to.lower())
        if not self.w3.isAddress(to):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong address")
        balance = await self._get_balance_contract(self.hot_wallet_addr)
        if balance < value:
            capture_message("No usdt on hot wallet")
            raise HTTPException(HTTPStatus.BAD_REQUEST, "No usdt on hot wallet")
        eth_balance = await self._get_eth_balance(to)
        if eth_balance < await self.get_actual_gasprice():
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Not enough gas")

        tx = self.contract.functions.transfer(to, int(value)).buildTransaction({
            "from": self.hot_wallet_addr,
            "nonce": self._get_nonce(),
            "gas": ETH_MAX_GAS_ETH_SEND,
            "gasPrice": await self.get_actual_gasprice(),
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

    async def loot_eth_from_wallets(self):
        wallets = await EthereumWalletCRUD.find_many({})

        for wallet in wallets:
            adr = wallet.get("eth_address")
            adr = self.w3.toChecksumAddress(adr.lower())
            contract_balance = await self._get_balance_contract(adr)
            if contract_balance > 0:
                continue
            ether_balance = await self._get_eth_balance(adr)
            actual_gasprice = await self.get_actual_gasprice()

            if ether_balance - (actual_gasprice * ETH_MAX_GAS_DEPOSIT_LOOT) <= 0:
                continue

            signed_txn = self.w3.eth.account.signTransaction(
                {
                    "from": adr,
                    "to": self.hot_wallet_addr,
                    "value": ether_balance - (actual_gasprice * ETH_MAX_GAS_DEPOSIT_LOOT),
                    "nonce": self._get_nonce_deposits(adr),
                    "gas": ETH_MAX_GAS_DEPOSIT_LOOT,
                    "gasPrice": actual_gasprice,
                },
                private_key=wallet.get("private_key")
            )
            tx_hash = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
            print(f"New transaction! {tx_hash}")
            time.sleep(2)
