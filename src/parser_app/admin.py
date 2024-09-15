from django.contrib import admin

# Register your models here.
from .models import HabrPostContent, HabrSourceURLs

admin.site.register(HabrSourceURLs)
admin.site.register(HabrPostContent)
