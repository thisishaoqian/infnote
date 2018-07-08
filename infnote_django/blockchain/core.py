import json

from bitcoin.rpc import Proxy
from bitcoin.core import script, b2lx, lx, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, CTransaction
from bitcoin.wallet import CBitcoinAddress
from binascii import unhexlify
from django.core.exceptions import ObjectDoesNotExist

from posts.models import Post
from utils.logger import default_logger as logger

from .models import Coin
from .serializers import PostSerializer

SERVER_ADDRESS = '1A6csP8jrpyruyW4a9tX9Nonv4R8AviB1y'


class Blockchain:
    def __init__(self):
        self.proxy = Proxy('http://rpcuser:111111@blockchain.infnote.com:8962')

    @staticmethod
    def deserialize_transaction(raw_tx):
        return CTransaction.deserialize(unhexlify(raw_tx.encode('utf8')))

    @classmethod
    def decode_transaction(cls, tx):
        contents = []
        for out in tx.vout:
            if out.nValue > 0:
                continue
            data, flag = cls.get_data_from_vout(out)
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
            return json.loads(data), flag
        return None, None

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
        txid = self.send_raw_to(address, coin.txid, coin.vout, coin.value)
        coin.frozen = True
        coin.save()
        return txid

    def send_raw_to(self, address, txid, vout, value):
        txin = CMutableTxIn(COutPoint(lx(txid), vout))
        txout = CMutableTxOut(value - 1e5, CBitcoinAddress(address).to_scriptPubKey())
        tx = CMutableTransaction([txin], [txout])
        tx = self.proxy.signrawtransaction(tx)['tx']

        # sig_hash = SignatureHash(txin_script_pubkey, tx, 0, SIGHASH_ALL)
        # sig = seckey.sign(sig_hash) + bytes([SIGHASH_ALL])
        # txin.scriptSig = CScript([sig, seckey.pub])
        # VerifyScript(txin.scriptSig, txin_script_pubkey, tx, 0, (SCRIPT_VERIFY_P2SH,))
        # print(b2x(tx.serialize()))

        return b2lx(self.proxy.sendrawtransaction(tx))


def transfer_a_coin_to(address):
    # TODO: 后期应该会用到多个币拼起来，需要修改为支持多个币
    coins = Coin.objects.filter(owner=SERVER_ADDRESS, spendable=True, frozen=False).order_by('id')
    if len(coins) > 0:
        c = coins[0]
        b = Blockchain()
        return b.send_coin_to(address, c)


def load_all_data(start, end):
    b = Blockchain()
    height = b.get_block_count()
    end = end if end and end < height else height
    for i in range(start, end + 1):
        block = b.get_block_by_height(i)
        save_tx_data(block, i)


def save_tx_data(block, height: int):
    for tx in block.vtx:
        for content in Blockchain.decode_transaction(tx):
            address = None
            for vin in tx.vin:
                if not vin.prevout.is_null():
                    coin = Coin.objects.get(txid=b2lx(vin.prevout.hash), vout=vin.prevout.n)
                    address = coin.owner
                    break
            content['date_confirmed'] = block.nTime
            content['is_confirmed'] = True
            content['transaction_id'] = b2lx(tx.GetTxid())
            content['block_height'] = height
            content['public_address'] = address

            try:
                post = Post.objects.get(transaction_id=content['transaction_id'])
                serializer = PostSerializer(instance=post, data=content)
            except ObjectDoesNotExist:
                serializer = PostSerializer(data=content)

            if serializer.is_valid():
                serializer.save()
                logger.info('Find post: %s', serializer.data['title'])
            else:
                for key, value in serializer.errors.items():
                    logger.warn('%s: %s', key, value)
