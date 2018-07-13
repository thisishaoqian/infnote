from bitcoin.core import b2lx
from bitcoin.wallet import CBitcoinAddress
from utils.logger import default_logger as logger
# from posts.models import Post
# from categories.models import Category

from .serializers import BaseCoinSerializer, BaseTransactionSerializer
from .models import *
from .core import Blockchain, Tool, script


def collect_transactions():
    blockchain = Blockchain()

    count = blockchain.get_block_count()
    start = Info.objects.get(id=1)
    logger.info('Blockchain count: %d' % count)
    logger.info('Fetching blocks from %d' % (start.height + 1))

    # 从上一次的高度 + 1 开始加载
    for height in range(start.height + 1, count + 1):
        block = blockchain.get_block_by_height(height)

        # 对于每一个 block 遍历里面所有的 tx
        for tx in block.vtx:
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
                    coin.spendable = False
                    coin.frozen = False
                    coin.spend_txid = newtx.id
                    coin.save()

            # 记录每一个 tx 的输入作为 Coin
            newtx.vout = []
            for i, v in enumerate(tx.vout):
                # nValue 大于 0 才代表是可以使用的钱
                _, flag = Blockchain.get_data_from_vout(v)
                if v.nValue > 0:
                    data = {
                        'txid': txid,
                        'vout': i,
                        'owner': str(CBitcoinAddress.from_scriptPubKey(v.scriptPubKey)),
                        'value': v.nValue,
                        'height': height,
                        'spendable': flag is None,  # TODO: 可能需要进一步确认是否可用
                        'frozen': False,
                        'is_confirmed': True,
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
        Tool.save_tx_data(block, height)

    start.height = count
    start.save()

    # 更新目录下的计数器
    # for category in Category.objects.all():
    #     ps = Post.objects.filter(category=category.name)
    #     posts = len(ps)
    #     topics = 0
    #     for post in ps:
    #         if post.reply_to is None:
    #             topics += 1
    #     category.posts = posts
    #     category.topics = topics
    #     category.save()

    logger.info('Successfully loaded all transactions.')
