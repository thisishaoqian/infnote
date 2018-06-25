from rest_framework import serializers

from .models import *


class BaseCoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = '__all__'


class BaseTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class CoinSerializer(BaseCoinSerializer):
    class Meta:
        model = Coin
        fields = ('txid', 'vout', 'value')
