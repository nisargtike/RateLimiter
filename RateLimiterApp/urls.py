from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseRedirect

urlpatterns = [
    url(r'^create-user/$', views.CreateUserAPI.as_view()),
    url(r'^delete-user/$', views.DeleteUserAPI.as_view()),
    url(r'^list-users/$', views.ListUsersAPI.as_view()),
    url(r'^test/$', views.TestAPI.as_view()),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)