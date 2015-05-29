from django.conf.urls import url, patterns


urlpatterns = patterns(
    'website.views',
    url(r'^$', 'index', name="index"),
    url(r"^register/$", 'register', name="register"),
    url(r"^login/$", 'user_login', name="login"),
    url(r"^organizer/$", 'organizer', name="organizer"),
    url(r"^organizer/organize/$", 'organize', name="organize"),
    url(r"^logout/$", 'organizer_logout', name="logout"),
    url(r"^contact/$", 'contact', name="contact"),
    url(r"^password_reset/$", 'password_reset', name="password_reset"),
    url(r"^change_password/$", 'change_password', name="change_password"),
    url(r"^search_tags/$", 'search_tags', name="search_tags")
)
