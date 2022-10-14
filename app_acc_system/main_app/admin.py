from django.contrib import admin
from .models import (Applications, ApplicationComments, Reports)


@admin.register(Applications)
class ApplicationsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'slug', 'client', 'subject', 'priority', 'type',
                    'status', 'deadline', 'executor', 'created_at']
    list_display_links = ['pk', 'slug']
    list_filter = ['client', 'priority', 'type', 'status', 'deadline', 'executor', 'created_at']
    search_fields = ['subject']
    save_as = True


@admin.register(ApplicationComments)
class ApplicationCommentsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'application', 'file', 'is_private', 'is_public', 'created_at']
    list_display_links = ['pk']
    list_filter = ['application', 'is_private', 'is_public', 'created_at']
    search_fields = ['application']
    save_as = True


@admin.register(Reports)
class ReportsAdmin(admin.ModelAdmin):
    list_display_links = ['pk', 'title']
    search_fields = ['title']
    list_display = ['pk', 'title', 'type', 'client', 'file', 'created_at']
    list_filter = ['created_at', 'type', 'client']
    save_as = True
