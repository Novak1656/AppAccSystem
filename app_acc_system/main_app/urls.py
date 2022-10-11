from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import ApplicationsListView, ApplicationCreateView

urlpatterns = [
    path('', login_required(ApplicationsListView.as_view()), name='app_list'),
    path('create/', login_required(ApplicationCreateView.as_view()), name='app_create'),

]
