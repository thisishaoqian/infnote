from bitcoin.rpc import Proxy
from bitcoin.core import CTransaction, script
from binascii import unhexlify
from json import loads


class Blockchain:
    def __init__(self):
        self.proxy = Proxy('http://rpcuser:111111@blockchain.infnote.com:8962')

    @staticmethod
    def deserialize_transaction(raw_tx):
        return CTransaction.deserialize(unhexlify(raw_tx.encode('utf8')))

    def decode_transaction(self, raw_tx):
        transaction = self.deserialize_transaction(raw_tx)
        for out in transaction.vout:
            i = iter(out.scriptPubKey)
            flag = next(i)
            if flag == script.OP_RETURN or flag == script.OP_NOP8:
                data = next(i).decode('utf8')
                return loads(data)

    def send_transaction(self, raw_tx):
        transaction = self.deserialize_transaction(raw_tx)
        txid = self.proxy.sendrawtransaction(transaction)
        return txid

    def server_unspent(self):
        return self.proxy.listunspent()


# if __name__ == '__main__':
#     from bitcoin.core import b2lx
#     unspents = Blockchain().server_unspent()
#     if len(unspents) > 0:
#         print(unspents[0])
