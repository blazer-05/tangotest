# -*- coding: UTF-8 -*-

import os

from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tangotest.settings')

import django
django.setup()

from rango.models import Category, Page


def populate():
    python_cat = add_cat('Python', views=128, likes=64)

    add_page(cat=python_cat,
        title="Official Python Tutorial",
        views = 20,
        likes = 45,
        url="http://docs.python.org/2/tutorial/")

    add_page(cat=python_cat,
        title="How to Think like a Computer Scientist",
        views = 20,
        likes = 45,
        url="http://www.greenteapress.com/thinkpython/")

    add_page(cat=python_cat,
        title="Learn Python in 10 Minutes",
        views = 20,
        likes = 45,
        url="http://www.korokithakis.net/tutorials/python/")

    django_cat = add_cat("Django", views=64, likes=32)

    add_page(cat=django_cat,
        title="Official Django Tutorial",
        views = 20,
        likes = 45,
        url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/")

    add_page(cat=django_cat,
        title="Django Rocks",
        views = 20,
        likes = 45,
        url="http://www.djangorocks.com/")

    add_page(cat=django_cat,
        title="How to Tango with Django",
        views = 20,
        likes = 45,
        url="http://www.tangowithdjango.com/")

    frame_cat = add_cat("Other Frameworks", views=32, likes=16)

    add_page(cat=frame_cat,
        title="Bottle",
        views = 20,
        likes = 45,
        url="http://bottlepy.org/docs/dev/")

    add_page(cat=frame_cat,
        title="Flask",
        views = 20,
        likes = 45,
        url="http://flask.pocoo.org")

    # Выводим на экран пользователю то, что мы добавили в базу
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print ('- {0} - {1}'.format(str(c), str(p)))

def add_page(cat, title, url, views=0, likes=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.likes=likes
    p.date = timezone.now()
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

# Код начинает выполняться отсюда!
if __name__ == '__main__':
    print ("Starting Rango population script...")
    populate()