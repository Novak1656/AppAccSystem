from django.contrib import admin
from .models import (Applications, ApplicationComments, ApplicationFiles, CommentsFiles)


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
    list_display = ['pk', 'application', 'is_private', 'is_public', 'created_at']
    list_display_links = ['pk']
    list_filter = ['application', 'is_private', 'is_public', 'created_at']
    search_fields = ['application']
    save_as = True


@admin.register(ApplicationFiles, CommentsFiles)
class FilesAdmin(admin.ModelAdmin):
    list_display_links = ['pk', 'slug']
    search_fields = ['title']
    save_as = True

    def get_list_display(self, request):
        if self.model == ApplicationFiles:
            return ['pk', 'slug', 'application', 'title', 'file']
        else:
            return ['pk', 'slug', 'comment', 'title', 'file']

    def get_list_filter(self, request):
        if self.model == ApplicationFiles:
            return ['application', 'title']
        else:
            return ['comment', 'title']
