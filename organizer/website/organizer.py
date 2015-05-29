from django.contrib.auth.hashers import make_password

import os
import hashlib
from datetime import datetime
from organizer.settings import SECRET_KEY, BASE_DIR
from cloud.helpers import dropbox
from .tagger import Tagger

from .models import Image, Category, Tag


class Organizer:

    def __init__(self, user, task):
        self._user = user
        self._task = task

    @property
    def task(self):
        return self._task

    def organize_personal_photos(self):
        photos = dropbox.Dropbox.get_user_photos(self._user)
        self.task.all_images = len(photos)
        self.task.save()

        for photo in photos:
            if len(Image.objects.filter(cloud_path=photo["path"], user=self._user)):
                self.task.progress += 1
                self.task.save()
                continue

            new_image = Image()
            new_image.user = self._user
            new_image.creation_date = self._get_modified_datetime(photo["modified"])
            new_image.rev = photo["rev"]
            new_image.bytes_size = photo["bytes"]
            new_image.cloud_path = photo["path"]
            image_path = self._get_photo_thumbnail(photo["path"])

            if not image_path:
                continue

            new_image.url = '/' + image_path
            content_id = Tagger.get_content_id(self._get_full_path(image_path))

            if content_id:
                category = Tagger.categorize_by_content_id(content_id)
                if not category:
                    continue

                new_image.category = self._add_category(category[0])
                new_image.category_confidence = category[1]

                tags = Tagger.tag_by_content_id(content_id)
                # print(tags)
                if not tags:
                    continue

                # Must be saved before many to many field is used
                new_image.save()
                for tag in tags:
                    t = self._add_tag(tag[0])
                    new_image.tags.add(t)

                new_image.organized = True
                new_image.save()

                self.task.progress += 1
                self.task.save()

    def _get_photo_thumbnail(self, photo_cloud_path):
        # hash email + id concatentation - random string
        # make it md5 so that it is shorter but still unique
        m = hashlib.md5()
        m.update(str(make_password(self._user.email + str(self._user.id), SECRET_KEY)).encode('utf-8'))
        user_photos_dir = 'static/users/%s' % m.hexdigest()

        if not os.path.isdir(self._get_full_path(user_photos_dir)):
            os.makedirs(self._get_full_path(user_photos_dir))

        photo_path = os.path.join(user_photos_dir, photo_cloud_path.split('/')[-1])

        photo_thumbnail = dropbox.Dropbox.get_photo_thumbnail(self._user, photo_cloud_path)

        if photo_thumbnail:
            with open(self._get_full_path(photo_path), 'wb+') as image_photo:
                image_photo.write(photo_thumbnail.read())

            photo_thumbnail.close()

            return photo_path

        return None

    def _get_full_path(self, relative_path):
        return os.path.join(BASE_DIR, 'website', relative_path)

    def _add_category(self, category_name):
        category = Category.objects.filter(name=category_name)
        if len(category):
            return category[0]

        category = Category(name=category_name)
        category.save()

        return category

    def _add_tag(self, tag_name):
        tag = Tag.objects.filter(tag=tag_name)
        if len(tag):
            return tag[0]

        tag = Tag(tag=tag_name)
        tag.save()

        return tag

    def _get_modified_datetime(self, modified):
        # Format dropbox's date and time into python datetime
        return datetime.strptime(modified, '%a, %d %b %Y %H:%M:%S +0000')
