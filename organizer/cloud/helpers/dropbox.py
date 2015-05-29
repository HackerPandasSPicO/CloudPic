import dropbox
from django.core.urlresolvers import reverse
from website.sending_settings import CLOUD_DATA
from cloud.models import Access

NAME = 'dropbox'


class Dropbox:

    @staticmethod
    def get_auth_flow(request, csrf=None):
        redirect_uri = request.build_absolute_uri(
            reverse('authorize_cloud', kwargs={'cloud_name': NAME}))
        return dropbox.client.DropboxOAuth2Flow(
            CLOUD_DATA[NAME]['key'],
            CLOUD_DATA[NAME]['secret'],
            redirect_uri,
            {
                'user': request.user.email,
                'dropbox-auth-csrf-token': (request.META['CSRF_COOKIE']
                                            if not csrf else csrf)
            },
            'dropbox-auth-csrf-token'
        )

    @staticmethod
    def get_saved_access_token(user):
        access = Access.objects.filter(
            user=user, access_type="dropbox")

        if len(access):
            return access[0].access_token

        return None

    @staticmethod
    def get_access_token(request):
        access_token = Dropbox.get_saved_access_token(request.user)
        if access_token:
            return access_token

        try:
            access_token, user_id, url_state = Dropbox.get_auth_flow(
                request, request.GET.get('state')).finish(request.GET)
            return access_token
        except dropbox.client.DropboxOAuth2Flow.BadRequestException:
            return False
        except dropbox.client.DropboxOAuth2Flow.BadStateException:
            return False
        except dropbox.client.DropboxOAuth2Flow.CsrfException:
            return False
        except dropbox.client.DropboxOAuth2Flow.NotApprovedException:
            return False
        except dropbox.client.DropboxOAuth2Flow.ProviderException:
            return False

    @staticmethod
    def get_user_photos(user):
        client = dropbox.client.DropboxClient(
            Dropbox.get_saved_access_token(user))
        result = client.search('/', '.jpg')
        return result

    @staticmethod
    def get_photo_thumbnail(user, photo_path):
        client = dropbox.client.DropboxClient(
            Dropbox.get_saved_access_token(user))
        thumbnail = client.thumbnail(photo_path, 'l')

        return thumbnail
