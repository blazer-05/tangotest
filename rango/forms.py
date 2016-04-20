# -*- coding: UTF-8 -*-
from django import forms
from django.contrib.auth.models import User

from rango.models import Category, Page, UserProfile


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the category name.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # Если url не пустое и не начинается с 'http://', вставить перед ним 'http://'.
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data

    class Meta:
        model = Page
        exclude = ('category',)
        fields = ('title', 'url', 'views')


# Чтобы реализовать функцию регистрации пользователя, необходимо выполнить следующие шаги:
#
#     Создать UserForm и UserProfileForm.
#     Добавить представление для обработки данных при создании нового пользователя.
#     Создать шаблон, который отображает UserForm и UserProfileForm.
#     Сопоставить URL созданному представлению.
#     Создать ссылку на страницу регистрации на главной странице

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')