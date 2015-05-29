from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# from django.core.mail import send_mail

import re
from cloud.helpers import dropbox
from website.send_new_password import generate_new_password, send_reset_password, send_feedback
from website.sending_settings import SENDER_EMAIL
from organizer import settings
from cloud.models import Access
from website.tagger import Tagger
from .models import Image, Category, OrganizingTask
from django.template import RequestContext

# Create your views here.
tagger = Tagger()


def organizer_logout(request):
    logout(request)
    return redirect("index")


def register(request):
    if request.user.is_authenticated():
        return redirect("organizer")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if _validate_register(username, email, password) is not True:
            password_error = _validate_register(username, email, password)
            return render(request, "register.html", locals())

        user = User.objects.create_user(username, email, password)
        return redirect("login")

    else:
        return render(request, "register.html", locals())


def _validate_register(username, email, password):
    if username is None or username.strip() == "":
        return False

    if email is None or email.strip() == "":
        return False

    if password is None or password.strip() == "":
        return False

    if not settings.DEBUG:
        if len(password) < 8:
            password_error = "Password too short! Must be at least 8 symbols."
            return password_error

        if not re.search('[a-zA-Z]', password):
            password_error = "Your password must contain upper and lower case characters!"
            return password_error

        if not re.search('[0-9]', password):
            password_error = "Your password must contain digits!"
            return password_error

    return True


def index(request):
    if request.user.is_authenticated():
        return redirect("organizer")

    return render(request, "index.html", locals())


def user_login(request):
    if request.user.is_authenticated():
        return redirect("organizer")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("organizer")
        else:
            # TODO: Make some message for this
            request.session['message'] = {
                'type': 1, 'content': "Wrong username or password!"}
            return redirect("login")

    else:
        return render(request, "login.html", locals())


def password_reset(request):
    if request.user.is_authenticated():
        return redirect("organizer")

    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            if user is not None:
                new_password = generate_new_password()
                send_reset_password(email, new_password)
                user.set_password(new_password)
                user.save()
                return redirect("login")
        except:
            reset_password_error = "Wrong E-mail!!"
            request.session['message'] = {
                'type': 1, 'content': "Wrong E-mail!"}
            return redirect("password_reset")
    else:
        return render(request, "password_reset.html", locals())


@login_required(login_url="login")
def organize(request):
    from .tasks import organize_personal_photos
    organize_personal_photos.delay(request.user)
    return redirect(reverse('organizer'))


@login_required(login_url="login")
def organizer(request):
    dropbox_access_token = dropbox.Dropbox.get_saved_access_token(request.user)

    task = OrganizingTask.objects.filter(user=request.user)
    if len(task):
        task = task[0]

    categories = settings.CATEGORIES
    # data = tagger.get_tags_for_pic_from_url(
    #     'http://nutritioncheckup.com/wp-content/uploads/2014/09/apple.jpg')
    return render(request, "organizer.html", locals())


def contact(request):
    if request.method == "POST":
        name = request.POST.get("sender_name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        send_feedback(SENDER_EMAIL, message, name, email)

    return render(request, "contact.html", locals())


@login_required(login_url="login")
def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        if not request.user.check_password(old_password):
            request.session['message'] = {
                'type': 1, 'content': "Wrong password!"}
            return redirect("change_password")
        if new_password == confirm_password:
            request.user.set_password(new_password)
            request.user.save()
            return redirect("organizer")
        else:
            request.session['message'] = {
                'type': 1, 'content': "Password doesn't match the confirmation!"
            }
            return redirect("change_password")

    else:
        return render(request, "change_password.html", locals())


@login_required(login_url="login")
def search_tags(request):
    if request.method == "POST":
        tag = request.POST.get("search-tags")
        tags_ids = Tag.objects.filter(tag_name__icontains=tag).values_list('id', flat=True)
        if len(tags_ids) > 0:
            current_user = request.user
            user_id = current_user.id
            image_ids = Image_Tag.objects.filter(tag__in=tags_ids).values_list('image_id', flat=True)
            images = Image.objects.filter(id__in=image_ids).filter(user_id=user_id)
        else:
            message = "No results found!"
    return render(request, "organizer.html", locals())


@login_required(login_url="login")
def categories(request, category_id):
    if request.method == "GET":
        current_user = request.user
        user_id = current_user.id
        category = Category.objects.filter(id=category_id).values_list('name', flat=True)
        if len(category) == 0:
            return redirect('organizer')
        category = category[0].replace('_', ' / ').title()

        images = Image.objects.filter(user_id=user_id).filter(category_id=category_id).order_by('-creation_date')
    return render(request, "category.html", locals())
