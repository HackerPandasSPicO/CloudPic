import dropbox
from django.core.urlresolvers import reverse
from organizer import settings
from cloud.models import Access


class Dropbox:

    name = 'dropbox'

    def __init__(self):
        self._cloud_data = settings.CLOUD_DATA[self.name]

    @property
    def cloud_data(self):
        return self._cloud_data

    def get_auth_flow(self, request, csrf=None):
        redirect_uri = request.build_absolute_uri(reverse('authorize_cloud', kwargs={'cloud_name': self.name}))
        return dropbox.client.DropboxOAuth2Flow(self._cloud_data['key'], self._cloud_data['secret'], redirect_uri,
                                                {'user': request.user.email, 'dropbox-auth-csrf-token': request.META['CSRF_COOKIE'] if not csrf else csrf},
                                                'dropbox-auth-csrf-token')

    def get_access_token(self, request):
        try:
            access_token, user_id, url_state = self.get_auth_flow(request, request.GET.get('state')).finish(request.GET)
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

    def get_user_photos(self, request):
        access = Access.objects.filter(user=request.user, access_type="dropbox")
        dropbox_access_token = access[0].access_token if len(access) else None

        client = dropbox.DropboxClient(dropbox_access_token)
        return client.search('/', '.jpeg')
