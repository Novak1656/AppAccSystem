from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *

urlpatterns = [
    path('', login_required(ClientsListView.as_view()), name='clients_list'),
    path('clients/add/', login_required(ClientCreateView.as_view()), name='client_create'),
    path('clients/detail/<str:client_slug>/', login_required(ClientDetailView.as_view()), name='client_detail'),
    path('clients/update/<str:client_slug>/', login_required(ClientUpdateView.as_view()), name='client_update'),

    path('clients/detail/<str:client_slug>/add/file/', login_required(ClientFilesCreateView.as_view()),
         name='client_create_file'),
    path('clients/files/delete/<str:file_slug>/', delete_client_file, name='delete_client_file'),

    path('clients/detail/<str:client_slug>/contact_persons/',
         login_required(ContactPersonsListView.as_view()), name='cp_list'),
    path('clients/detail/<str:client_slug>/contact_persons/add',
         login_required(ContactPersonCreateView.as_view()), name='cp_create'),
    path('contact_persons/detail/<int:pk>/',
         login_required(ContactPersonDetailView.as_view()), name='cp_detail'),
    path('contact_persons/detail/<int:pk>/update/',
         login_required(ContactPersonUpdateView.as_view()), name='cp_update'),
    path('contact_persons/detail/<int:cp_pk>/delete/', contact_person_delete, name='cp_delete'),
]
