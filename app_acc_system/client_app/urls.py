from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *

urlpatterns = [
    path('', login_required(ClientsListView.as_view()), name='clients_list'),
    path('add/', login_required(ClientCreateView.as_view()), name='client_create'),
    path('detail/<str:client_slug>/', login_required(ClientDetailView.as_view()), name='client_detail'),
    path('update/<str:client_slug>/', login_required(ClientUpdateView.as_view()), name='client_update'),
    path('delete/<str:client_slug>/', client_delete_view, name='client_delete_view'),

    path('detail/<str:client_slug>/add/file/', login_required(ClientFilesCreateView.as_view()),
         name='client_create_file'),
    path('files/delete/<str:file_slug>/', delete_client_file, name='delete_client_file'),


    path('detail/<str:client_slug>/contact_persons/',
         login_required(ContactPersonsListView.as_view()), name='cp_list'),
    path('detail/<str:client_slug>/contact_persons/add',
         login_required(ContactPersonCreateView.as_view()), name='cp_create'),
    path('contact_persons/detail/<int:pk>/',
         login_required(ContactPersonDetailView.as_view()), name='cp_detail'),
    path('contact_persons/detail/<int:pk>/update/',
         login_required(ContactPersonUpdateView.as_view()), name='cp_update'),
    path('contact_persons/detail/<int:cp_pk>/delete/', contact_person_delete, name='cp_delete'),


    path('detail/<str:client_slug>/contracts/', login_required(ContractsListView.as_view()), name='cont_list'),
    path('detail/<str:client_slug>/contracts/add',
         login_required(ContractsCreateView.as_view()), name='cont_create'),
    path('contracts/detail/<str:cont_slug>/', login_required(ContractsDetailView.as_view()), name='cont_detail'),
    path('contracts/detail/<str:cont_slug>/update/', login_required(ContractsUpdateView.as_view()), name='cont_update'),
    path('contracts/detail/<str:cont_slug>/delete/', contracts_delete_view, name='cont_delete'),

    path('contracts/detail/<str:cont_slug>/add/file/', login_required(ContractFilesCreateView.as_view()),
         name='cont_create_file'),
    path('contracts/files/delete/<str:file_slug>/', delete_cont_file, name='delete_cont_file'),


    path('settings/equipment_types/', login_required(EquipmentTypeListCreateView.as_view()), name='e_types_list'),
    path('settings/equipment_types/<int:pk>/delete/', equipment_type_delete, name='e_types_delete'),
    path('settings/equipment_types/<int:pk>/update/', login_required(EquipmentTypeUpdateView.as_view()),
         name='e_types_update'),

    path('settings/equipment_attributes/', login_required(EquipmentAttributeListView.as_view()), name='e_attrs_list'),
    path('settings/equipment_attributes/create/',
         login_required(EquipmentAttributeCreateView.as_view()), name='e_attrs_create'),
    path('settings/equipment_attributes/<int:pk>/delete/', delete_equipment_attributes, name='e_attrs_delete'),
    path('settings/equipment_attributes/<int:pk>/update/', login_required(EquipmentAttributeUpdateView.as_view()),
         name='e_attrs_update'),


    path('detail/<str:client_slug>/equipments/', login_required(EquipmentsListView.as_view()), name='eq_list'),
    path('detail/<str:client_slug>/equipments/create',
         login_required(EquipmentsCreateView.as_view()), name='eq_create'),
    path('equipments/detail/<str:eq_slug>/', login_required(EquipmentsDetailView.as_view()), name='eq_detail'),
    path('equipments/detail/<str:eq_slug>/update/', login_required(EquipmentsUpdateView.as_view()), name='eq_update'),
    path('equipments/detail/<str:eq_slug>/delete/', equipments_delete_view, name='eq_delete'),

    path('equipments/detail/<str:eq_slug>/add/file/', login_required(EquipmentFilesCreateView.as_view()),
         name='eq_create_file'),
    path('equipments/files/delete/<str:file_slug>/', delete_eq_file, name='delete_eq_file'),
]
