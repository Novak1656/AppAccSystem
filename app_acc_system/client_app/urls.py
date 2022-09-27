from django.urls import path
from .views import *

urlpatterns = [
    path('', ClientsListView.as_view(), name='clients_list'),
    path('clients/add/', ClientCreateView.as_view(), name='client_create'),
]
