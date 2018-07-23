from utils.logger import default_logger as logger

from .models import *
from .core import Blockchain, Tool


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
            blockchain.save_tx(tx, height)
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
