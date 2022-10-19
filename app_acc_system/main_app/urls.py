from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *

urlpatterns = [
    path('', login_required(ApplicationsListView.as_view()), name='app_list'),
    path('application/create/', login_required(ApplicationCreateView.as_view()), name='app_create'),
    path('application/detail/<str:app_slug>/', login_required(ApplicationDetailView.as_view()), name='app_detail'),
    path('application/delete/<str:app_slug>/', delete_application, name='app_delete'),

    path('reports/', login_required(ReportsListView.as_view()), name='reports_list'),

    path('reports/generate_report/client/', report_client_create_view, name='generate_client_report'),
    path('reports/generate_report/clients/', report_clients_create_view, name='generate_clients_report'),
    path('reports/generate_report/executors/', report_executors_create_view, name='generate_executors_report'),
    path('reports/delete_report/', delete_report_view, name='delete_report'),

    path('application/set_executor/<str:app_slug>/', set_application_executor, name='set_application_executor'),
    path('application/delete_comment/<int:comment_pk>/', delete_comment, name='delete_comment'),
    path('application/update_comment/<int:comment_pk>/', update_comment_body, name='update_comment'),
    path('application/change_status/<str:app_slug>/', change_application_status, name='change_application_status'),
]
