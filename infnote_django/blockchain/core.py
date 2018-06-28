from bitcoin.rpc import Proxy
from bitcoin.core import CTransaction, script
from binascii import unhexlify
import json

SERVER_ADDRESS = '1A6csP8jrpyruyW4a9tX9Nonv4R8AviB1y'
SERVER_PRIVATE_KEY = '5K48NE3WCt6mcAQur693L7QrpvjYLJkAuTX2jkvzLAit9LkJQRk'


class Blockchain:
    def __init__(self):
        self.proxy = Proxy('http://rpcuser:111111@blockchain.infnote.com:8962')

    @staticmethod
    def deserialize_transaction(raw_tx):
        return CTransaction.deserialize(unhexlify(raw_tx.encode('utf8')))

    def decode_transaction(self, raw_tx):
        transaction = self.deserialize_transaction(raw_tx)
        return [self.get_data_from_vout(out) for out in transaction.vout]

    def send_transaction(self, raw_tx):
        transaction = self.deserialize_transaction(raw_tx)
        txid = self.proxy.sendrawtransaction(transaction)
        return txid

    @staticmethod
    def get_data_from_vout(vout):
        i = iter(vout.scriptPubKey)
        flag = next(i)
        if flag == script.OP_RETURN or flag == script.OP_NOP8:
            data = next(i).decode('utf8')
            return json.loads(data)

    def get_transaction(self, txid):
        return self.proxy.getrawtransaction(txid)

    def get_block_count(self):
        return self.proxy.getblockcount()

    def get_block_hash_by_height(self, height: int):
        return self.proxy.getblock(self.proxy.getblockhash(height))

    def server_unspent(self):
        return self.proxy.listunspent()

    def send_coin_to(self, adddress, coin):
        pass
