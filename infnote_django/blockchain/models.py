from djongo import models


class Block(models.Model):
    _id = models.ObjectIdField()
    hash = models.CharField()
    prev_hash = models.CharField(null=True, blank=True)
    time = models.IntegerField()
    signature = models.CharField()
    chain_id = models.CharField()
    height = models.IntegerField()
    payload = models.BinaryField()

    class Meta:
        db_table = 'blocks'
        app_label = 'blockchain'
        managed = False
