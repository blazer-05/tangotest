# -*- coding: UTF-8 -*-
from django.contrib import admin
from rango.models import Category, Page, UserProfile


class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'url', 'date']
    list_filter = ['date']

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name', 'views', 'likes', 'slug']




admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)

admin.site.register(UserProfile)



