from djongo import models


class Category(models.Model):
    id = models.ObjectIdField(db_column='_id', default=None)
    name = models.CharField(max_length=20, db_index=True)
    display_name = models.CharField(max_length=100, null=True)
    desc = models.CharField(max_length=255, null=True)
    topics = models.IntegerField(default=0)
    posts = models.IntegerField(default=0)

    # 占位用
    def last_topic(self):
        return self.name

    class Meta:
        db_table = 'infnote_categories'
