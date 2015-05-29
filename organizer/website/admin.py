from django.contrib import admin

from .models import Image, Category, Tag, OrganizingTask

admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(OrganizingTask)
