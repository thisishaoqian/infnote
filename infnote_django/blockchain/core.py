import json

from datetime import datetime
from pytz import timezone

from bitcoin.rpc import Proxy
from bitcoin.core import script, b2lx, lx, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, CTransaction
from bitcoin.wallet import CBitcoinAddress
from binascii import unhexlify
from django.core.exceptions import ObjectDoesNotExist

from users.models import User
from posts.models import Post
from utils.logger import default_logger as logger

from .models import Coin, Transaction
from .serializers import PostSerializer, UserSerializer, BaseCoinSerializer, BaseTransactionSerializer


SERVER_ADDRESS = '1A6csP8jrpyruyW4a9tX9Nonv4R8AviB1y'
MONEY_UNIT = 1e8
TX_FEE = 1e5


class Blockchain:
    def __init__(self):
        self.proxy = Proxy('http://rpcuser:111111@blockchain.infnote.com:8962')

    @staticmethod
    def deserialize_transaction(raw_tx):
        return CTransaction.deserialize(unhexlify(raw_tx.encode('utf8')))

    @staticmethod
    def address_in_vout(vout):
        return str(CBitcoinAddress.from_scriptPubKey(vout.scriptPubKey))

    @staticmethod
    def address_in_vin(vin):
        if not vin.prevout.is_null():
            try:
                coin = Coin.objects.get(txid=b2lx(vin.prevout.hash), vout=vin.prevout.n)
                address = coin.owner
                return address
            except ObjectDoesNotExist:
                return None
        return None

    @classmethod
    def decode_transaction(cls, tx):
        contents = []
        for out in tx.vout:
            if out.nValue > 0:
                continue
            data, flag = cls.get_data_from_vout(out)
            if data:
                contents.append((data, flag))
            else:
                contents.append((None, None))
        return contents

    def send_transaction(self, raw_tx):
        transaction = self.deserialize_transaction(raw_tx)
        txid = self.proxy.sendrawtransaction(transaction)
        self.save_tx(transaction)
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
        txout = CMutableTxOut(value - TX_FEE, CBitcoinAddress(address).to_scriptPubKey())
        tx = CMutableTransaction([txin], [txout])
        tx = self.proxy.signrawtransaction(tx)['tx']

        # sig_hash = SignatureHash(txin_script_pubkey, tx, 0, SIGHASH_ALL)
        # sig = seckey.sign(sig_hash) + bytes([SIGHASH_ALL])
        # txin.scriptSig = CScript([sig, seckey.pub])
        # VerifyScript(txin.scriptSig, txin_script_pubkey, tx, 0, (SCRIPT_VERIFY_P2SH,))
        # print(b2x(tx.serialize()))

        txid = b2lx(self.proxy.sendrawtransaction(tx))
        self.save_tx(tx)
        return txid

    @classmethod
    def save_tx(cls, tx, height=0):
        txid = b2lx(tx.GetTxid())
        txsrlzr = BaseTransactionSerializer(data={
            'id': txid,
            'vin': [],
            'vout': [],
            'height': height,
        })
        if txsrlzr.is_valid():
            newtx = txsrlzr.save()
        else:
            # 不清除数据库也可以更新
            newtx = Transaction.objects.get(id=txid)

        # 记录每一个 tx 输入
        newtx.vin = []
        for v in tx.vin:
            # 如果是挖出来的矿则没有输入
            if not v.prevout.is_null():
                # 找到输入的 tx
                t = Transaction.objects.get(id=b2lx(v.prevout.hash))
                # 前 tx 的 vout 里应有对应的输出
                coin_id = t.vout[v.prevout.n]
                # 插入新 tx 的输入
                newtx.vin.append(coin_id)
                # 处理以 (txid, vout) 对应的 Coin
                coin = Coin.objects.get(id=coin_id)
                coin.spendable = height == 0
                coin.frozen = height == 0
                coin.spend_txid = newtx.id
                coin.save()

        # 记录每一个 tx 的输入作为 Coin
        newtx.vout = []
        for i, v in enumerate(tx.vout):
            # nValue 大于 0 才代表是可以使用的钱
            _, flag = cls.get_data_from_vout(v)
            if v.nValue > 0:
                data = {
                    'txid': txid,
                    'vout': i,
                    'owner': str(CBitcoinAddress.from_scriptPubKey(v.scriptPubKey)),
                    'value': v.nValue,
                    'height': height,
                    'spendable': flag is None,
                    'frozen': False,
                    'is_confirmed': height != 0,
                }
                serializer = BaseCoinSerializer(data=data)
                if serializer.is_valid():
                    coin = serializer.save()
                else:
                    # 不清除数据库也可以更新
                    coin = Coin.objects.get(txid=data['txid'], vout=i)
                newtx.vout.append(coin.id)
            else:
                # 占位
                if flag == script.OP_RETURN:
                    newtx.vout.append(-1)
                elif flag == script.OP_NOP8:
                    newtx.vout.append(-2)
                else:
                    newtx.vout.append(-1000)
        newtx.save()


class Tool:

    @classmethod
    def transfer_a_coin_to(cls, address):
        # TODO: 后期应该会用到多个币拼起来，需要修改为支持多个币
        coins = Coin.objects.filter(owner=SERVER_ADDRESS, spendable=True, frozen=False).order_by('id')
        if len(coins) > 0:
            c = coins[0]
            b = Blockchain()
            return b.send_coin_to(address, c)

    @classmethod
    def load_all_data(cls, start, end):
        b = Blockchain()
        height = b.get_block_count()
        end = end if end and end < height else height
        for i in range(start, end + 1):
            block = b.get_block_by_height(i)
            cls.save_tx_data(block, i)

    @classmethod
    def save_tx_data(cls, block, height: int):
        for tx in block.vtx:
            cls.save_post_data(tx, block.nTime, height) or \
                cls.save_userinfo(tx) or \
                cls.confirm_userinfo(tx, block.nTime)

    @classmethod
    def save_userinfo(cls, tx):
        if len(tx.vout) < 2:
            return False
        if Blockchain.address_in_vout(tx.vout[1]) != SERVER_ADDRESS or tx.vout[1].nValue < TX_FEE * 2:
            return False

        content, flag = Blockchain.get_data_from_vout(tx.vout[0])
        if not content or flag != script.OP_NOP8:
            return False

        content['date_confirmed'] = None
        content['is_confirmed'] = False
        content['info_txid'] = b2lx(tx.GetTxid())
        content['confirm_txid'] = None
        content['public_address'] = Blockchain.address_in_vin(tx.vin[0])

        try:
            user = User.objects.get(public_address=content['public_address'])
            serializer = UserSerializer(instance=user, data=content, partial=True)
        except ObjectDoesNotExist:
            content['password'] = '123456'
            content['private_key'] = None
            serializer = UserSerializer(data=content)

        if serializer.is_valid():
            serializer.save()
            logger.info('Found user: %s, %s', serializer.data['email'], serializer.data['public_address'])
        else:
            for key, value in serializer.errors.items():
                logger.warn('%s: %s', key, value)
            return False

        return True

    @classmethod
    def confirm_userinfo(cls, tx, time):
        if len(tx.vin) != 1:
            return False
        if Blockchain.address_in_vin(tx.vin[0]) != SERVER_ADDRESS:
            return False

        info_txid = b2lx(tx.vin[0].prevout.hash)
        confirm_txid = b2lx(tx.GetTxid())
        try:
            user = User.objects.get(info_txid=info_txid)
            user.is_confirmed = True
            user.date_confirmed = timezone('UTC').localize(datetime.utcfromtimestamp(time))
            user.confirm_txid = confirm_txid
            user.save()
        except ObjectDoesNotExist:
            return False

        logger.info('Confirmed user: %s, %s', user.email, user.public_address)
        return True

    @classmethod
    def save_post_data(cls, tx, time, height):
        content, flag = Blockchain.get_data_from_vout(tx.vout[0])
        if not content or flag != script.OP_RETURN:
            return False

        content['date_confirmed'] = time
        content['is_confirmed'] = True
        content['transaction_id'] = b2lx(tx.GetTxid())
        content['block_height'] = height
        content['public_address'] = Blockchain.address_in_vin(tx.vin[0])

        try:
            post = Post.objects.get(transaction_id=content['transaction_id'])
            serializer = PostSerializer(instance=post, data=content)
        except ObjectDoesNotExist:
            serializer = PostSerializer(data=content)

        if serializer.is_valid():
            serializer.save()
            logger.info('Found post: %s', serializer.data['title'])
        else:
            for key, value in serializer.errors.items():
                logger.warn('%s: %s', key, value)
            return False

        return True

