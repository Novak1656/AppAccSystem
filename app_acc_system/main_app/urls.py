from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import ApplicationsListView, ApplicationCreateView, ApplicationDetailView, set_application_executor

urlpatterns = [
    path('', login_required(ApplicationsListView.as_view()), name='app_list'),
    path('application/create/', login_required(ApplicationCreateView.as_view()), name='app_create'),
    path('application/detail/<str:app_slug>/', login_required(ApplicationDetailView.as_view()), name='app_detail'),

    path('application/set_executor/<str:app_slug>/', set_application_executor, name='set_application_executor'),
]
