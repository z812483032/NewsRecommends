from django.db import models


# Create your models here.
class user(models.Model):
    userid = models.CharField(primary_key=True, max_length=30)
    region = models.CharField(max_length=30)
    username = models.CharField(max_length=50)
    gender = models.IntegerField()
    # active inactive
    ip = models.GenericIPAddressField()
    password = models.CharField(max_length=20)
    tags = models.CharField(max_length=2000)
    tagsweight = models.CharField(max_length=2000)
    headPortrait = models.CharField(max_length=255)
    objects = models.Manager()


class newsdetail(models.Model):
    news_id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    date = models.CharField(max_length=30)
    pic_url = models.CharField(max_length=1000)
    videourl = models.CharField(max_length=200)
    mainpage = models.CharField(max_length=2000)
    origin = models.CharField(max_length=2000)
    category = models.IntegerField()
    readnum = models.IntegerField()
    comments = models.IntegerField()
    keywords = models.CharField(max_length=1000)
    objects = models.Manager()


class hotword(models.Model):
    hotword = models.CharField(max_length=50)
    num = models.IntegerField()
    objects = models.Manager()

class recommend(models.Model):
    userid = models.IntegerField(primary_key=True)
    newsid = models.IntegerField()
    hadread = models.IntegerField()
    cor = models.FloatField()
    species = models.IntegerField()
    time = models.CharField(max_length=30)
    objects = models.Manager()

class newssimilar(models.Model):
    new_id_base = models.CharField(primary_key=True, max_length=64)
    new_id_sim = models.CharField(max_length=64)
    new_correlation = models.FloatField()
    objects = models.Manager()

class comments(models.Model):
    id = models.AutoField(primary_key=True)
    newsid = models.IntegerField()
    comments = models.CharField(max_length=1000)
    userid = models.IntegerField()
    touserid = models.IntegerField()
    time = models.DateTimeField()
    status = models.CharField(max_length=20)
    objects = models.Manager()

class history(models.Model):
    userid = models.IntegerField()
    history_newsid = models.IntegerField()
    time = models.DateTimeField()
    id = models.AutoField(primary_key=True)
    objects = models.Manager()

class newshot(models.Model):
    news_id = models.IntegerField(primary_key=True)
    news_hot = models.FloatField()
    category = models.IntegerField()
    objects = models.Manager()

class givelike(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.IntegerField()
    newsid = models.IntegerField()
    givelikeornot = models.IntegerField()
    objects = models.Manager()

class message(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.IntegerField()
    message = models.CharField(max_length=1000)
    time = models.CharField(max_length=30)
    newsid = models.IntegerField()
    hadread = models.IntegerField()
    title = models.CharField(max_length=255)
    objects = models.Manager()

class spiderstate(models.Model):
    spiderid = models.IntegerField(primary_key=True)
    status = models.IntegerField()
    interval = models.CharField(max_length=30)
    objects = models.Manager()

class urlcollect(models.Model):
    url = models.CharField(primary_key=True, max_length=255)
    handle = models.IntegerField()
    type = models.IntegerField()
    time = models.CharField(max_length=30)
    objects = models.Manager()
