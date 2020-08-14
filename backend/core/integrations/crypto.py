from web3 import Web3
from passlib import pwd

from config import INFURA_URL


class EthereumWrapper:
    def __init__(self):
        self.w3 = Web3(Web3.WebsocketProvider(INFURA_URL))

    async def create_wallet(self):
        entropy = pwd.genword()
        account = self.w3.eth.account.create(entropy)
        return (
            account.address,
            account.privateKey.hex(),
            entropy
        )

