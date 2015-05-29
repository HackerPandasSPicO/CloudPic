from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):

    user = models.ForeignKey(User)
    url = models.CharField(max_length=500)


class Tag(models.Model):

    tag_name = models.CharField(max_length=50, unique=True)


class Image_Tag(models.Model):

    image = models.ForeignKey(Image)
    tag = models.ForeignKey(Tag)
