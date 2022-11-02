import os
import shutil

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from ..forms import ClientForm, ClientFilesForms
from ..models import Clients, ClientFiles
from ..services import chek_access_rights


class ClientsListView(AccessMixin, ListView):
    model = Clients
    template_name = 'client_app/clients_page.html'
    login_url = reverse_lazy('stuff_user_auth')
    context_object_name = 'clients'

    def get_queryset(self):
        return Clients.objects.all().annotate(
            cp_count=Count('contact_persons', distinct=True),
            eq_count=Count('equipments', distinct=True),
            ct_count=Count('contracts', distinct=True),
        )

    def dispatch(self, request, *args, **kwargs):
        chek_access_rights(request.user)
        return super(ClientsListView, self).dispatch(request, *args, **kwargs)


class ClientCreateView(AccessMixin, CreateView):
    model = Clients
    template_name = 'client_app/add_client.html'
    login_url = reverse_lazy('stuff_user_auth')
    success_url = reverse_lazy('clients_list')
    form_class = ClientForm

    def dispatch(self, request, *args, **kwargs):
        chek_access_rights(request.user)
        return super(ClientCreateView, self).dispatch(request, *args, **kwargs)


class ClientDetailView(AccessMixin, DetailView):
    model = Clients
    template_name = 'client_app/client_detail.html'
    context_object_name = 'client'
    login_url = reverse_lazy('stuff_user_auth')
    slug_url_kwarg = 'client_slug'

    def dispatch(self, request, *args, **kwargs):
        chek_access_rights(request.user)
        return super(ClientDetailView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Clients.objects.filter(slug=self.kwargs['client_slug']).annotate(
            cp_count=Count('contact_persons', distinct=True),
            eq_count=Count('equipments', distinct=True),
            ct_count=Count('contracts', distinct=True),
        )

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        context['client_files'] = ClientFiles.objects.select_related('client').filter(client=self.object).all()
        return context


class ClientUpdateView(AccessMixin, UpdateView):
    model = Clients
    template_name = 'client_app/client_update.html'
    form_class = ClientForm
    login_url = reverse_lazy('stuff_user_auth')
    slug_url_kwarg = 'client_slug'

    def get_success_url(self):
        return reverse_lazy('client_detail', kwargs={'client_slug': self.object.slug})

    def form_valid(self, form):
        client_obj = Clients.objects.get(slug=self.kwargs['client_slug'])
        if client_obj.name != self.object.name:
            files = client_obj.files.all()
            old_file_path = os.path.join(settings.BASE_DIR, f"media/User_files/{client_obj.name}/")
            self.object = form.save(commit=False)
            for obj in files:
                obj.file.name = os.path.join(f"User_files/{self.object.name}/{obj.filename}")
                obj.save()
            new_file_path = os.path.join(settings.BASE_DIR, f"media/User_files/{self.object.name}/")
            os.rename(old_file_path, new_file_path)
            self.object.save()
        return super(ClientUpdateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        chek_access_rights(request.user)
        return super(ClientUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ClientUpdateView, self).get_context_data(**kwargs)
        context['client_name'] = self.object.name
        context['form'] = self.form_class(instance=self.object)
        return context


@login_required
def client_delete_view(request, client_slug):
    chek_access_rights(request.user)
    client = Clients.objects.get(slug=client_slug).delete()
    if client.files.exists():
        files_path = os.path.join(settings.BASE_DIR, f"media/User_files/{client.name}/")
        shutil.rmtree(files_path)
    return redirect('clients_list')


class ClientFilesCreateView(AccessMixin, CreateView):
    model = ClientFiles
    template_name = 'client_app/add_client_file.html'
    form_class = ClientFilesForms
    login_url = reverse_lazy('stuff_user_auth')
    slug_url_kwarg = 'client_slug'

    def get_success_url(self):
        return reverse_lazy('client_detail', kwargs={'client_slug': self.kwargs['client_slug']})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.client = get_object_or_404(Clients, slug=self.kwargs['client_slug'])
        self.object.save()
        return super(ClientFilesCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        chek_access_rights(request.user)
        return super(ClientFilesCreateView, self).dispatch(request, *args, **kwargs)


@login_required
def delete_client_file(request, file_slug):
    chek_access_rights(request.user)
    client_file = get_object_or_404(ClientFiles, slug=file_slug)
    client_file.delete()
    return redirect(request.META['HTTP_REFERER'])
