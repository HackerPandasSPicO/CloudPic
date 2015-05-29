from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from .helpers import dropbox
from cloud.models import Access


def connect_cloud(request, cloud_name):
    if request.method == "GET":
        if cloud_name == "dropbox":
            auth_flow = dropbox.Dropbox.get_auth_flow(request)

            return HttpResponseRedirect(auth_flow.start())

    return HttpResponseNotFound("Not found.")


def authorize_cloud(request, cloud_name):
    if request.method == "GET":
        if cloud_name == "dropbox":
            access_token = dropbox.Dropbox.get_access_token(request)

            if access_token:
                # Add access token to Access model
                access = Access(user=request.user, access_token=access_token)
                access.save()

                return redirect(reverse('organizer'))
            else:
                return HttpResponse("A problem occurred. Try again.")

    return HttpResponseNotFound("Not found.")
