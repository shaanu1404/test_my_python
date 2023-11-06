from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import UserApp

class UserAppAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'app_url', 'app_qr_code', 'created_at']

    def app_qr_code(self, obj):
        return mark_safe(f'<img src="{obj.qr_code.url}" alt="{obj.app_url}" style="width: 80px; height: 80px; object-fit: contain;" />')
    app_qr_code.allow_tags = True
    app_qr_code.short_description = 'App QR code'

admin.site.register(UserApp, UserAppAdmin)