from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):

    user = models.ForeignKey(User)
    url = models.CharField(max_length=500)
    creation_date = models.DateTimeField()
    rev = models.CharField(max_length=40)
    bytes_size = models.IntegerField(default=0)
    cloud_path = models.CharField(max_length=500)
    organized = models.BooleanField(default=False)

    tags = models.ManyToManyField('Tag')
    category = models.ForeignKey('Category')
    category_confidence = models.FloatField(default=0.0)

    def __str__(self):
        return self.url


class Tag(models.Model):

    tag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag


class Category(models.Model):

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class OrganizingTask(models.Model):

    user = models.ForeignKey(User)
    progress = models.IntegerField(default=0)
    all_images = models.IntegerField(default=0)
