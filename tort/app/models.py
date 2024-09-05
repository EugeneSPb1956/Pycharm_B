from tortoise import fields, models

class Artists(models.Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=50, unique=True)
    country = fields.CharField(max_length=15, default='N/A')
    city = fields.CharField(max_length=15, default='N/A')
    year1 = fields.IntField(null=True)
    year2 = fields.IntField(null=True)
    active = fields.BooleanField(default=True)
    # date_created = fields.DatetimeField(auto_now_add=True)
    # date_updated = fields.DatetimeField(auto_now=True)

    name_link: fields.ForeignKeyRelation['Albums']

    class Meta:
        table = 'artists'

    def __str__(self):
        return 'Исполнители'

class Albums(models.Model):
    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=100)

    # artists_id = fields.ForeignKeyField()  # .ForeignKey(Artists, on_delete=models.CASCADE)
    # studio_id = models.IntegerField()
    # studio_id = models.ForeignKey(Studio, on_delete=models.CASCADE)
    lable = fields.CharField(max_length=15, default='N/A')
    release = fields.IntField(null=True)
    genre = fields.CharField(max_length=10, default='N/A')
    price = fields.DecimalField(max_digits=11, null=True, decimal_places=2)

    # artist = fields.CharField(max_length=50)
    artists: fields.ForeignKeyField(model_name='models.Artists',
                                     related_name='name_link',
                                     on_delete=fields.CASCADE,)

    def __str__(self):
        return 'Альбомы'

    class Meta:
        table = 'albums'
