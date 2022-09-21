from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('user/login/', stuff_user_auth, name='stuff_user_auth'),
    path('user/logout/', stuff_user_logout, name='stuff_user_logout'),

    path('', login_required(StuffUsersListView.as_view()), name='stuff_list'),
    path('create/', login_required(StuffUserCreateView.as_view()), name='stuff_create'),
    path('<str:username>/detail/', stuff_user_detail, name='stuff_detail'),

    path('change_user_status/<int:user_pk>/', change_user_status, name='change_user_status'),
    path('user/config/new_login/<int:user_pk>/', stuff_user_change_login, name='stuff_user_change_login'),
    path('user/config/new_password/<int:user_pk>/', stuff_user_change_password, name='stuff_user_change_password'),
    path('user/delete/<int:user_pk>/', stuff_user_delete, name='stuff_user_delete'),
]
