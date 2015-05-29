from django.db import models
from django.contrib.auth.models import User
import operator


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

    @property
    def pretty_name(self):
        return self.name.replace('_', ' / ').title()

    @staticmethod
    def get_user_categories(user):
        all_categories = Category.objects.all()
        user_categories = {}
        for category in all_categories:
            user_images = Image.objects.filter(user=user, category=category)

            if len(user_images):
                user_images = user_images.order_by('-category_confidence')
                user_categories[category] = user_images[:4]

        return sorted(
            user_categories.items(),
            key=lambda x: -len(Image.objects.filter(user=user, category=x[0]))
        )


class OrganizingTask(models.Model):

    user = models.ForeignKey(User)
    progress = models.IntegerField(default=0)
    all_images = models.IntegerField(default=0)
