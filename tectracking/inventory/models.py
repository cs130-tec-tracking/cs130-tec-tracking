from django.db import models

class Asset(models.Model):
    serial_num = models.CharField(max_length=8, primary_key=True, db_column='serial_no', verbose_name='serial number')
    bar_code = models.IntegerField(unique=True, db_column='bar_code_id')
    rfid = models.IntegerField(null=True, blank=True)
    asset_model_mfg = models.CharField(max_length=10, verbose_name='model manufacturer')
    asset_model_type = models.CharField(max_length=15, verbose_name='model type')
    asset_model_name = models.CharField(max_length=8, verbose_name='model name')
    amt_memory = models.SmallIntegerField(null=True, blank=True, verbose_name='amount memory')
    num_cores = models.SmallIntegerField(null=True, blank=True, db_column='no_cores', verbose_name='number of cores')

    categories = models.ManyToManyField('Category', through='AssetCategory')

    class Meta:
        db_table = 'inventory_source'

    def __unicode__(self):
        return self.serial_num

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, verbose_name='category')

    class Meta:
        db_table = 'asset_category'
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name

class AssetCategory(models.Model):
    asset = models.ForeignKey(Asset, db_column='serial_no')
    category = models.ForeignKey(Category, db_column='category_id',)

    class Meta:
        db_table = 'asset_categories'
        verbose_name_plural = 'asset categories'

    def __unicode__(self):
        return '%s | %s' % (self.asset.serial_num, self.category.name)

class Note(models.Model):
    note_id = models.AutoField(primary_key=True)
    asset = models.ForeignKey(Asset, db_column='serial_no')
    message = models.TextField()

    class Meta:
        db_table = 'asset_note'
