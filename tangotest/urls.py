# -*- coding: UTF-8 -*-
"""tangotest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url, patterns

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from rango import views
from rango.views import index
from registration.backends.simple.views import RegistrationView

# Создайте новый класс, который перенаправит пользователя на главную страницу при успешной регистрации



class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return '/rango/add_profile/'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rango/', include('rango.urls')),
    # Добавляем эту строку в URL шаблоны, чтобы переопределить шаблон, используемый по умолчанию для учетных записей, - r'^accounts/'.
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^accounts/user/profile/$', views.profile, name='profile'),
]
# urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
         'serve',
         {'document_root': settings.MEDIA_ROOT}),
    )


# from django.conf.urls.static import static
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from tangotest import settings
# #
# # if settings.DEBUG:
# #     urlpatterns += staticfiles_urlpatterns()+ static(
# #     settings.MEDIA_URL, document_root = settings.MEDIA_ROOT
# #     )
# #
# if settings.DEBUG:
#     if settings.MEDIA_ROOT:
#         urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# urlpatterns += staticfiles_urlpatterns()
