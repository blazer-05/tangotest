# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify


class Category(models.Model):
    class Meta():
        db_table = 'app_category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(max_length=128, unique=True, verbose_name='Имя')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    likes = models.IntegerField(default=0, verbose_name='Лайки')
    slug = models.SlugField(unique=True, verbose_name='Транслит')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name



class Page(models.Model):
    class Meta():
        db_table = 'app_page'
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    category = models.ForeignKey(Category, verbose_name='Категория')
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    url = models.URLField(verbose_name='Ссылка')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    likes = models.IntegerField(default=0, verbose_name='Лайки')
    date = models.DateTimeField(blank=True, null=True, verbose_name='Дата')

    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
    class Meta():
        db_table = 'userprofile'
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профиль пользователей'
    # Эта строка обязательна. Она связывает UserProfile с экземпляром модели User.
    user = models.OneToOneField(User)
    # Дополнительные атрибуты, которые мы хотим добавить.
    website = models.URLField(blank=True, verbose_name='Веб сайт')
    picture = models.ImageField(upload_to='profile_images', blank=True, verbose_name='Изображение')

    def __unicode__(self):
        return self.user.username