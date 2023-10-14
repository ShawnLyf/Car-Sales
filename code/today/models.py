# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse

class Carmodel(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'carmodel'
        unique_together = (('brand', 'model'),)
    
    def __str__(self):
        
        return str(self.id)


class Post(models.Model):
    id = models.BigIntegerField(primary_key=True)  # The composite primary key (id, is_active) found, that is not supported. The first column is selected.
    is_active = models.BooleanField()
    title = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    createtime = models.DateTimeField()
    updatetime = models.CharField(max_length=20, blank=True, null=True)
    lastrequest_time = models.DateTimeField(blank=True, null=True)
    postcity = models.TextField(blank=True, null=True)  # This field type is a guess.
    views = models.SmallIntegerField(blank=True, null=True)
    mileage = models.BigIntegerField(blank=True, null=True)
    is_auto = models.BooleanField(blank=True, null=True)
    regodue = models.CharField(max_length=20, blank=True, null=True)
    suburb = models.CharField(max_length=50, blank=True, null=True)
    video = models.CharField(max_length=300, blank=True, null=True)
    year = models.SmallIntegerField(blank=True, null=True)
    prevprice = models.IntegerField(blank=True, null=True)
    boughtyear = models.SmallIntegerField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    fueltype = models.TextField(blank=True, null=True)  # This field type is a guess.
    lastservice = models.CharField(max_length=20, blank=True, null=True)
    likes = models.SmallIntegerField(blank=True, null=True)
    reviews = models.TextField(blank=True, null=True)  # This field type is a guess.
    images = models.TextField(blank=True, null=True)  # This field type is a guess.
    carmodel = models.ForeignKey('Carmodel', models.DO_NOTHING, blank=True, null=True)
    seller_username = models.ForeignKey('Seller', models.DO_NOTHING, db_column='seller_username', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post'
        unique_together = (('id', 'is_active'),)
    
    def get_absolute_url(self):
        return reverse("detail", args=[self.id])
    

class PostTag(models.Model):
    postid = models.ForeignKey('Post', models.DO_NOTHING, db_column='postid')
    post_isactive = models.BooleanField()
    tagid = models.ForeignKey('Tag', models.DO_NOTHING, db_column='tagid')

    class Meta:
        managed = False
        db_table = 'post_tag'
        unique_together = (('postid', 'post_isactive', 'tagid'),)


class Seller(models.Model):
    username = models.CharField(primary_key=True, max_length=50)
    is_private = models.BooleanField(blank=True, null=True)
    userage = models.DateField(blank=True, null=True)
    userimage = models.CharField(max_length=300, blank=True, null=True)
    phones = models.TextField(blank=True, null=True)  # This field type is a guess.
    wechats = models.TextField(blank=True, null=True)  # This field type is a guess.
    qqs = models.TextField(blank=True, null=True)  # This field type is a guess.
    emails = models.TextField(blank=True, null=True)  # This field type is a guess.
    contacts = models.SmallIntegerField(blank=True, null=True)
    reports = models.SmallIntegerField(blank=True, null=True)
    dealerage = models.SmallIntegerField(blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    dealertitle = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    business = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'seller'

    def __str__(self):
        return self.username


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    tagname = models.TextField()  # This field type is a guess.
    class Meta:
        managed = False
        db_table = 'tag'
