from django.conf.urls import url, patterns


urlpatterns = patterns(
    'cloud.views',
    url(r"^(?P<cloud_name>\w+)/connect/$", 'connect_cloud', name="connect_cloud"),
    url(r"^(?P<cloud_name>\w+)/authorize/$", 'authorize_cloud', name="authorize_cloud")
)
