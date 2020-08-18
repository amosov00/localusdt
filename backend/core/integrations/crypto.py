from typing import Tuple, List
import ujson
from os import path
from web3 import Web3
from web3.middleware import geth_poa_middleware
from passlib import pwd
from decimal import Decimal

from database.crud.transaction import USDTTransactionCRUD
from config import (
    BASE_DIR,
    INFURA_URL_TESTNET,
    INFURA_URL_MAINNET,
    IS_PRODUCTION,
    ABI_FILEPATH_MAINNET,
    ABI_FILEPATH_TESTNET,
    USDT_CONTRACT_ADDRESS_MAINNET,
    USDT_CONTRACT_ADDRESS_TESTNET
)


class USDTWrapper:
    def __init__(self):
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

    async def parse_last_blocks(self, last_blocks: int) -> List[dict]:
        last_block_number: int = self.w3.eth.getBlock("latest").get("number")
        tx_hashes = set()
        transactions_in_db = await USDTTransactionCRUD.find_many({})
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

