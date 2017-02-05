# -*- coding: UTF-8 -*-
from django.conf.urls import url
from rango import views
from rango.views import index_rango, about


urlpatterns = [
    url(r'^$', index_rango, name='index_rango'),
    url(r'^about/', about, name='about'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^add_category/', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^search/', views.search, name='search'),
    url(r'^goto/', views.track_url, name='track_url'),
    url(r'^add_profile/', views.register_profile, name='register_profile'),
    url(r'^like_category/$', views.like_category, name='like_category'),
    url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
    url(r'^auto_add_page/$', views.auto_add_page, name='auto_add_page'),




    # url(r'^register/$', views.register, name='register'),
    # url(r'^login/$', views.user_login, name='user_login'),
    # url(r'^restricted/', views.restricted, name='restricted'),
    # url(r'^logout/$', views.user_logout, name='logout'),
    # url(r'^tags/', tags, name='tags'),


]



