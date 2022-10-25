from django.contrib import admin
from .models import StuffUsers, StuffUsersNotifications

admin.site.site_title = 'Application accounting system'
admin.site.site_header = 'Application accounting system'


@admin.register(StuffUsers)
class StuffUsersAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'username', 'first_name', 'second_name',
        'last_name', 'role', 'status', 'created_at',
        'updated_at', 'notifications_active', 'is_superuser'
    ]
    list_display_links = ['id', 'username']
    list_filter = ['role', 'status', 'created_at', 'is_superuser']


@admin.register(StuffUsersNotifications)
class StuffUsersNotificationsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'notify_subject', 'notify_text', 'created_at']
    list_display_links = ['id', 'user']
    list_filter = ['user', 'notify_subject', 'created_at']
