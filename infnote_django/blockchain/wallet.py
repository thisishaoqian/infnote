from rest_framework.views import APIView
from rest_framework.response import Response

from .core import Blockchain

from bitcoin.core import b2lx


class Unspent(APIView):
    blockchain = Blockchain()

    def get(self, _):
        unspents = self.blockchain.server_unspent()
        count = len(unspents)
        if count > 0:
            return Response({
                'txid': b2lx(unspents[0]['outpoint'].hash),
                'amount': unspents[0]['amount'],
                'fee': 1e5,
                'count': count
            })
        else:
            return Response({
                'count': 0
            })
