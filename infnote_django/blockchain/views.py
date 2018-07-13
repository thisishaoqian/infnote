from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .core import MONEY_UNIT, TX_FEE
from .models import Coin
from .serializers import CoinSerializer


class Balance(APIView):

    permission_classes = [IsAuthenticated]

    # TODO: 缓存用户余额，缓存更新策略有待考虑
    @staticmethod
    def get(request):
        balance = 0
        frozen = 0
        unconfirmed = 0
        for coin in Coin.objects.filter(owner=request.user.public_address).all():
            if coin.spendable:
                balance += coin.value
            if not coin.is_confirmed:
                unconfirmed += coin.value
            if coin.frozen:
                frozen += coin.value
        return Response({
            'balance': balance,
            'frozen': frozen,
            'unconfirmed': unconfirmed,
            'unit': MONEY_UNIT,
        })


class GetCoin(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        value = int(request.query_params.get('value', 0))
        confirmed = bool(request.query_params.get('confirmed', True))

        coins = []
        amount = 0
        queryset = Coin.objects.filter(
            owner=request.user.public_address,
            spendable=True,
            frozen=False,
            is_confirmed=confirmed,
        ).order_by('id').all()

        for coin in queryset:
            data = CoinSerializer(coin).data
            # data['value'] /= 1e8
            coins.append(data)
            amount += coin.value
            if amount >= value + TX_FEE:
                return Response({'coins': coins, 'fee': TX_FEE})

        return Response({'message': 'You have no coin avaliable.'}, status=status.HTTP_400_BAD_REQUEST)
