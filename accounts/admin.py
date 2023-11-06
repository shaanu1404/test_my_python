from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import UserProfile


@register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass
