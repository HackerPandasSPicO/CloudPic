from django.db import models
from django.contrib.auth.models import User


class Access(models.Model):

    user = models.ForeignKey(User, related_name='access_tokens')
    access_token = models.CharField(max_length=100)
    access_type = models.CharField(max_length=20, default="dropbox")
