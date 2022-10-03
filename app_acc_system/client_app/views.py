import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .models import *
from .forms import ClientForm, ClientFilesForms, ContactPersonsForms

# Пересмотреть все запросы во воьюшках tак как слаг это считай пк
class ClientsListView(AccessMixin, ListView):
    model = Clients
    template_name = 'client_app/clients_page.html'
    login_url = reverse_lazy('stuff_user_auth')
    context_object_name = 'clients'

    def dispatch(self, request, *args, **kwargs):
        if request.user.role == 'executor':
            raise Http404
        return super(ClientsListView, self).dispatch(request, *args, **kwargs)


class ClientCreateView(AccessMixin, CreateView):
    model = Clients
    template_name = 'client_app/add_client.html'
    login_url = reverse_lazy('stuff_user_auth')
    success_url = reverse_lazy('clients_list')
    form_class = ClientForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ClientCreateView, self).dispatch(request, *args, **kwargs)


class ClientDetailView(AccessMixin, DetailView):
    model = Clients
    template_name = 'client_app/client_detail.html'
    context_object_name = 'client'
    login_url = reverse_lazy('stuff_user_auth')
    slug_url_kwarg = 'client_slug'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ClientDetailView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Clients.objects.filter(slug=self.kwargs['client_slug']).annotate(
            cp_count=Count('contact_persons'),
            eq_count=Count('equipments'),
            ct_count=Count('contracts'),
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

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ClientUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ClientUpdateView, self).get_context_data(**kwargs)
        context['client_name'] = self.object.name
        context['form'] = self.form_class(instance=self.object)
        return context


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
        if not request.user.is_staff:
            raise Http404
        return super(ClientFilesCreateView, self).dispatch(request, *args, **kwargs)


@login_required
def delete_client_file(request, file_slug):
    if not request.user.is_staff:
        raise Http404
    client_file = get_object_or_404(ClientFiles, slug=file_slug)
    file_path = client_file.file.path
    os.remove(file_path)
    client_file.delete()
    return redirect(request.META['HTTP_REFERER'])


class ContactPersonsListView(AccessMixin, ListView):
    model = ContactPersons
    template_name = 'client_app/contact_persons_list.html'
    login_url = reverse_lazy('stuff_user_auth')
    context_object_name = 'contact_persons'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ContactPersonsListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return ContactPersons.objects.select_related('client').filter(client__slug=self.kwargs['client_slug']).all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ContactPersonsListView, self).get_context_data(**kwargs)
        context['client'] = get_object_or_404(Clients, slug=self.kwargs['client_slug'])
        return context


class ContactPersonCreateView(AccessMixin, CreateView):
    model = ContactPersons
    template_name = 'client_app/contact_persons_create.html'
    login_url = reverse_lazy('stuff_user_auth')
    form_class = ContactPersonsForms

    def get_success_url(self):
        return reverse_lazy('cp_list', kwargs={'client_slug': self.kwargs['client_slug']})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.client = get_object_or_404(Clients, slug=self.kwargs['client_slug'])
        self.object.save()
        return super(ContactPersonCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ContactPersonCreateView, self).dispatch(request, *args, **kwargs)


class ContactPersonDetailView(AccessMixin, DetailView):
    model = ContactPersons
    template_name = 'client_app/contact_persons_detail.html'
    context_object_name = 'contact_person'
    login_url = reverse_lazy('stuff_user_auth')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ContactPersonDetailView, self).dispatch(request, *args, **kwargs)