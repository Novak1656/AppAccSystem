from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.models import Group
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .forms import StuffUserCreateForm, StuffUserInfoForm, StuffUserLoginChangeForm, StuffUserLoginForm
from .models import StuffUsers


def is_staff_chek(user):
    if not user.is_staff:
        raise Http404
    return


class StuffUserCreateView(AccessMixin, CreateView):
    model = StuffUsers
    template_name = 'stuff_app/add_executor.html'
    form_class = StuffUserCreateForm
    login_url = reverse_lazy('stuff_user_auth')
    success_url = reverse_lazy('stuff_list')
    
    def dispatch(self, request, *args, **kwargs):
        is_staff_chek(self.request.user)
        return super(StuffUserCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        stuff_user = form.save()
        group = Group.objects.get(name=stuff_user.role)
        stuff_user.groups.add(group)
        stuff_user.save()
        return super(StuffUserCreateView, self).form_valid(form)


class StuffUsersListView(AccessMixin, ListView):
    model = StuffUsers
    template_name = 'stuff_app/executors_page.html'
    context_object_name = 'executors'
    login_url = reverse_lazy('stuff_user_auth')


@login_required
def stuff_user_detail(request, username):
    is_staff_chek(request.user)
    executor = StuffUsers.objects.get(username=username)
    if request.method == 'POST':
        form = StuffUserInfoForm(request.POST, instance=executor)
        if form.is_valid():
            form.save()
            return redirect(executor.get_absolute_url())
    else:
        form = StuffUserInfoForm(instance=executor)
    return render(request, 'stuff_app/detail_executor.html', {'executor': executor, 'form': form})


@login_required
def change_user_status(request, user_pk):
    is_staff_chek(request.user)
    user = StuffUsers.objects.get(pk=user_pk)
    if user.status == 'Active':
        user.status = 'Archive'
        user.save()
    else:
        user.status = 'Active'
        user.save()
    return redirect(user.get_absolute_url())


@login_required
def stuff_user_change_login(request, user_pk):
    is_staff_chek(request.user)
    user = StuffUsers.objects.get(pk=user_pk)
    if request.method == 'POST':
        form = StuffUserLoginChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(user.get_absolute_url())
    else:
        form = StuffUserLoginChangeForm()
    return render(request, 'stuff_app/change_login.html', {'form': form})


@login_required
def stuff_user_change_password(request, user_pk):
    is_staff_chek(request.user)
    user = StuffUsers.objects.get(pk=user_pk)
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=user)
        if form.is_valid():
            form.save()
            return redirect(user.get_absolute_url())
    else:
        form = PasswordChangeForm(user=user)
    return render(request, 'stuff_app/change_password.html', {'form': form})


@login_required
def stuff_user_delete(request, user_pk):
    is_staff_chek(request.user)
    user = StuffUsers.objects.get(pk=user_pk)
    user.delete()
    return redirect('stuff_list')


def stuff_user_auth(request):
    if request.method == 'POST':
        form = StuffUserLoginForm(data=request.POST)
        print(request.POST)
        if form.is_valid():
            user = form.get_user()
# Нихуя блять не работает эта ёбаная параша если сменить статус пользователю блять
            if not user.is_active:
                print('op')
                messages.error(request, 'Ваша учетная запись заблокирована, обратитесь к администратору системы')
            else:
                login(request, user)
                return redirect('stuff_list')
    else:
        form = StuffUserLoginForm()
    return render(request, 'stuff_app/login_page.html', {'form': form})


def stuff_user_logout(request):
    logout(request)
    return redirect('stuff_user_auth')
