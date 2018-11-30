from djongo import models


class Migration(models.Model):
    chain_id = models.CharField(max_length=256, unique=True)
    height = models.IntegerField(default=0)

    class Meta:
        db_table = 'infnote_migration'
