from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):

    user_id = models.ForeignKey(User)
    url = models.CharField(max_length=500)


class Tag(models.Model):

    tag_name = models.CharField(max_length=50, unique=True)


class Image_Tag(models.Model):

    image_id = models.ForeignKey(Image)
    tag_id = models.ForeignKey(Tag)
