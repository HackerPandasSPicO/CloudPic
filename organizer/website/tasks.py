from __future__ import absolute_import

from celery import shared_task
from .models import OrganizingTask
from .organizer import Organizer


@shared_task
def organize_personal_photos(user):
    if not len(OrganizingTask.objects.filter(user=user)):
        task = OrganizingTask(user=user)
        task.save()

        try:
            org = Organizer(user, task)
            org.organize_personal_photos()
        except:
            pass

        task.delete()
