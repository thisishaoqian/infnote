from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Coin
from .serializers import CoinSerializer

UNIT = 1e8
FEE = 1e5


class Balance(APIView):

    permission_classes = [IsAuthenticated]

    # TODO: 缓存用户余额，缓存更新策略有待考虑
    @staticmethod
    def get(request):
        balance = 0
        for coin in Coin.objects.filter(owner=request.user.public_address, spendable=True).all():
            balance += coin.value
        return Response({'balance': balance, 'unit': UNIT})


class GetCoin(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        value = int(request.query_params.get('value', 0))

        coins = []
        amount = 0
        queryset = Coin.objects.filter(
            owner=request.user.public_address,
            spendable=True,
            frozen=False
        ).order_by('id').all()

        for coin in queryset:
            data = CoinSerializer(coin).data
            # data['value'] /= 1e8
            coins.append(data)
            amount += coin.value
            if amount >= value:
                return Response({'coins': coins, 'fee': FEE})

        return Response({'message': 'You have no coin avaliable.'}, status=status.HTTP_400_BAD_REQUEST)
