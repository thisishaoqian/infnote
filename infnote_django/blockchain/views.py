from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Coin
from .serializers import CoinSerializer


class Balance(APIView):

    permission_classes = [IsAuthenticated]

    # TODO: 缓存用户余额，缓存更新策略有待考虑
    @staticmethod
    def get(request):
        balance = 0
        for coin in Coin.objects.filter(owner=request.user.public_address, spendable=True).all():
            balance += coin.value
        return Response({'balance': balance, 'unit': 1e8})


class GetCoin(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        value = int(request.query_params.get('value', 0))
        spend = bool(request.query_params.get('spend', False))

        coins = []
        amount = 0
        queryset = Coin.objects.filter(
            owner=request.user.public_address,
            spendable=True,
            frozen=False
        ).all()

        for coin in queryset:
            if spend:
                coin.spending = True
                coin.save()
            data = CoinSerializer(coin).data
            # data['value'] /= 1e8
            coins.append(data)
            amount += coin.value
            if amount >= value:
                return Response({'coins': coins, 'fee': 1e5})
