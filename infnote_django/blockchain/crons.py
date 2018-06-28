from bitcoin.core import b2lx
from bitcoin.wallet import CBitcoinAddress
from .serializers import BaseCoinSerializer, BaseTransactionSerializer
from .models import *
from .core import Blockchain

from utils.logger import get_logger

logger = get_logger('bitcoin')


def collect_transactions():
    blockchain = Blockchain()

    count = blockchain.get_block_count()
    start = Info.objects.get(id=1)
    logger.info('Blockchain count: %d' % count)
    logger.info('Fetching blocks from %d' % (start.height + 1))

    for height in range(start.height + 1, count + 1):
        block = blockchain.get_block_by_height(height)
        for tx in block.vtx:
            txid = b2lx(tx.GetTxid())
            txsrlzr = BaseTransactionSerializer(data={
                'id': txid,
                'vin': [],
                'vout': []
            })
            if txsrlzr.is_valid():
                newtx = txsrlzr.save()
            else:
                newtx = Transaction.objects.get(id=txid)

            for v in tx.vin:
                newtx.vin = []
                if not v.prevout.is_null():
                    t = Transaction.objects.get(id=b2lx(v.prevout.hash))
                    coin_id = t.vout[v.prevout.n]
                    newtx.vin.append(coin_id)
                    coin = Coin.objects.get(id=coin_id)
                    coin.spendable = False
                    coin.frozen = False
                    coin.save()

            for i, v in enumerate(tx.vout):
                newtx.vout = []
                if v.nValue > 0:
                    data = {
                        'txid': txid,
                        'vout': i,
                        'owner': str(CBitcoinAddress.from_scriptPubKey(v.scriptPubKey)),
                        'value': v.nValue,
                        'height': height,
                        'spendable': True,
                        'frozen': False,
                    }
                    serializer = BaseCoinSerializer(data=data)
                    if serializer.is_valid():
                        coin = serializer.save()
                    else:
                        coin = Coin.objects.get(txid=data['txid'], vout=i)
                    newtx.vout.append(coin.id)
                # else:
                #     print(blockchain.get_data_from_vout(v))
            newtx.save()

    start.height = count
    start.save()

    logger.info('Successfully loaded all transactions.')
