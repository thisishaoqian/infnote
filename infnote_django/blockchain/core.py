from bitcoin.rpc import Proxy
from bitcoin.core import script, b2lx, lx, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, CTransaction
from bitcoin.wallet import CBitcoinAddress
from binascii import unhexlify
import json

from .models import Coin

SERVER_ADDRESS = '1A6csP8jrpyruyW4a9tX9Nonv4R8AviB1y'
SERVER_PRIVATE_KEY = '5K48NE3WCt6mcAQur693L7QrpvjYLJkAuTX2jkvzLAit9LkJQRk'


class Blockchain:
    def __init__(self):
        self.proxy = Proxy('http://rpcuser:111111@blockchain.infnote.com:8962')

    @staticmethod
    def deserialize_transaction(raw_tx):
        return CTransaction.deserialize(unhexlify(raw_tx.encode('utf8')))

    def decode_transaction(self, tx):
        contents = []
        for out in tx.vout:
            if out.nValue > 0:
                continue
            data = self.get_data_from_vout(out)
            if data:
                contents.append(data)
        return contents

    def send_transaction(self, raw_tx):
        transaction = self.deserialize_transaction(raw_tx)
        txid = self.proxy.sendrawtransaction(transaction)
        return txid

    @staticmethod
    def get_data_from_vout(vout):
        i = iter(vout.scriptPubKey)
        flag = next(i)
        # TODO: 需要区分类型，以填充至不同的模型
        if flag == script.OP_RETURN or flag == script.OP_NOP8:
            data = next(i).decode('utf8')
            return json.loads(data)
        return None

    def get_transaction(self, txid):
        return self.proxy.getrawtransaction(txid)

    def get_block_count(self):
        return self.proxy.getblockcount()

    def get_block_by_height(self, height: int):
        return self.proxy.getblock(self.proxy.getblockhash(height))

    def server_unspent(self):
        return self.proxy.listunspent()

    @staticmethod
    def freeze_coins_in_tx(tx: CTransaction):
        for vin in tx.vin:
            coin = Coin.objects.get(txid=b2lx(vin.prevout.hash), vout=vin.prevout.n)
            coin.frozen = True
            coin.save()

    def send_coin_to(self, address, coin: Coin):
        txin = CMutableTxIn(COutPoint(lx(coin.txid), coin.vout))
        txout = CMutableTxOut(coin.value - 1e5, CBitcoinAddress(address).to_scriptPubKey())
        tx = CMutableTransaction([txin], [txout])
        tx = self.proxy.signrawtransaction(tx)['tx']

        # sig_hash = SignatureHash(txin_script_pubkey, tx, 0, SIGHASH_ALL)
        # sig = seckey.sign(sig_hash) + bytes([SIGHASH_ALL])
        # txin.scriptSig = CScript([sig, seckey.pub])
        # VerifyScript(txin.scriptSig, txin_script_pubkey, tx, 0, (SCRIPT_VERIFY_P2SH,))
        # print(b2x(tx.serialize()))

        self.proxy.sendrawtransaction(tx)
        coin.frozen = True
        coin.save()


def send_a_coin_to(address):
    # TODO: 后期应该会用到多个币拼起来，需要修改为支持多个币
    coins = Coin.objects.filter(owner=SERVER_ADDRESS, spendable=True, frozen=False).order_by('id')
    if len(coins) > 0:
        c = coins[0]
        b = Blockchain()
        b.send_coin_to(address, c)


def load_all_data(start):
    b = Blockchain()
    height = b.get_block_count()
    for i in range(start, height + 1):
        block = b.get_block_by_height(i)
        for tx in block.vtx:
            for content in b.decode_transaction(tx):
                print(content)
