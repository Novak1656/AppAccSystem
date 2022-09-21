from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stuff/', include('stuff_app.urls')),
    path('client/', include('client_app.urls')),
    path('', include('main_app.urls')),

]

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
