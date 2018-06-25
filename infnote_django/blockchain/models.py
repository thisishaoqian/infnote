from djongo import models


class Coin(models.Model):

    txid = models.CharField(max_length=64, db_index=True)
    vout = models.IntegerField(default=0)
    value = models.BigIntegerField(default=0)
    spendable = models.BooleanField(default=False)
    frozen = models.BooleanField(default=False)

    # User.public_address
    owner = models.CharField(max_length=34)

    height = models.IntegerField(default=0)

    class Meta:
        db_table = 'bc_coin'
        unique_together = ('txid', 'vout')


class Transaction(models.Model):

    id = models.CharField(max_length=64, primary_key=True, unique=True)
    vin = models.ListField()
    vout = models.ListField()

    class Meta:
        db_table = 'bc_tx'


class Info(models.Model):
    height = models.IntegerField(default=-1)

    class Meta:
        db_table = 'bc_info'
