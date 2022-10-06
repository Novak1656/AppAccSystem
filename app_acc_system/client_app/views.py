import os
import shutil

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.core.files import File
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .models import *
from .forms import ClientForm, ClientFilesForms, ContactPersonsForms, ContractsForms, ContractsFilesForms, \
    EquipmentTypeForms, EquipmentAttributeForms


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


class ContactPersonUpdateView(AccessMixin, UpdateView):
    model = ContactPersons
    template_name = 'client_app/contact_persons_update.html'
    login_url = reverse_lazy('stuff_user_auth')
    form_class = ContactPersonsForms
    
    def get_success_url(self):
        return reverse_lazy('cp_detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ContactPersonUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContactPersonUpdateView, self).get_context_data(**kwargs)
        context['cp_name'] = self.object.get_full_name
        context['form'] = self.form_class(instance=self.object)
        return context


@login_required
def contact_person_delete(request, cp_pk):
    if not request.user.is_staff:
        raise Http404
    cp_obj = ContactPersons.objects.get(pk=cp_pk)
    client_slug = cp_obj.client.slug
    cp_obj.delete()
    return redirect('cp_list', client_slug=client_slug)


class ContractsListView(AccessMixin, ListView):
    model = Contracts
    template_name = 'client_app/contracts_list.html'
    context_object_name = 'contracts'
    login_url = reverse_lazy('stuff_user_auth')

    def get_queryset(self):
        return Contracts.objects.select_related('client').filter(client__slug=self.kwargs['client_slug'])

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ContractsListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ContractsListView, self).get_context_data(**kwargs)
        context['client'] = get_object_or_404(Clients, slug=self.kwargs['client_slug'])
        return context


class ContractsDetailView(AccessMixin, DetailView):
    model = Contracts
    template_name = 'client_app/contracts_detail.html'
    login_url = reverse_lazy('stuff_user_auth')
    context_object_name = 'contract'
    slug_url_kwarg = 'cont_slug'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ContractsDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContractsDetailView, self).get_context_data(**kwargs)
        context['cont_files'] = self.object.files.all()
        return context


class ContractsCreateView(AccessMixin, CreateView):
    model = Contracts
    template_name = 'client_app/contracts_create.html'
    form_class = ContractsForms
    login_url = reverse_lazy('stuff_user_auth')

    def get_success_url(self):
        return reverse_lazy('cont_list', kwargs={'client_slug': self.kwargs['client_slug']})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.client = get_object_or_404(Clients, slug=self.kwargs['client_slug'])
        self.object.save()
        return super(ContractsCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ContractsCreateView, self).dispatch(request, *args, **kwargs)


class ContractsUpdateView(AccessMixin, UpdateView):
    model = Contracts
    template_name = 'client_app/contracts_update.html'
    form_class = ContractsForms
    slug_url_kwarg = 'cont_slug'
    login_url = reverse_lazy('stuff_user_auth')

    def get_success_url(self):
        return reverse_lazy('cont_detail', kwargs={'cont_slug': self.object.slug})
    
    def form_valid(self, form):
        cont_obj = Contracts.objects.prefetch_related('files').get(slug=self.kwargs['cont_slug'])
        if cont_obj.title != self.object.title:
            files = cont_obj.files.all()
            old_file_path = os.path.join(settings.BASE_DIR, f"media/Contract_files/{cont_obj.title}/")
            self.object = form.save(commit=False)
            new_file_path = os.path.join(settings.BASE_DIR, f"media/Contract_files/{self.object.title}/")
            os.rename(old_file_path, new_file_path)
            for obj in files:
                obj.file.name = os.path.join(f"Contract_files/{self.object.title}/{obj.filename}")
                obj.save()
            self.object.save()
        return super(ContractsUpdateView, self).form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ContractsUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContractsUpdateView, self).get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context


@login_required
def contracts_delete_view(request, cont_slug):
    if not request.user.is_staff:
        raise Http404
    contract = get_object_or_404(Contracts, slug=cont_slug)
    client_slug = contract.client.slug
    if contract.files.exists():
        files_path = os.path.join(settings.BASE_DIR, f"media/Contract_files/{contract.title}/")
        shutil.rmtree(files_path)
    contract.delete()
    return redirect('cont_list', client_slug=client_slug)


class ContractFilesCreateView(AccessMixin, CreateView):
    model = ContractFiles
    template_name = 'client_app/contracts_create_file.html'
    slug_url_kwarg = 'cont_slug'
    login_url = reverse_lazy('stuff_user_auth')
    form_class = ContractsFilesForms

    def get_success_url(self):
        return reverse_lazy('cont_detail', kwargs={'cont_slug': self.kwargs['cont_slug']})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.contract = get_object_or_404(Contracts, slug=self.kwargs['cont_slug'])
        self.object.save()
        return super(ContractFilesCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ContractFilesCreateView, self).dispatch(request, *args, **kwargs)


@login_required
def delete_cont_file(request, file_slug):
    if not request.user.is_staff:
        raise Http404
    file_obj = get_object_or_404(ContractFiles, slug=file_slug)
    cont_slug = file_obj.contract.slug
    file_obj.delete()
    return redirect('cont_detail', cont_slug=cont_slug)


class EquipmentTypeListCreateView(AccessMixin, CreateView):
    model = EquipmentType
    template_name = 'client_app/equipment_type_list.html'
    form_class = EquipmentTypeForms
    login_url = reverse_lazy('stuff_user_auth')
    success_url = reverse_lazy('e_types_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(EquipmentTypeListCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EquipmentTypeListCreateView, self).get_context_data(**kwargs)
        context['equipment_types'] = self.model.objects.all()
        return context


class EquipmentTypeUpdateView(AccessMixin, UpdateView):
    model = EquipmentType
    template_name = 'client_app/equipment_type_update.html'
    form_class = EquipmentTypeForms
    login_url = reverse_lazy('stuff_user_auth')
    success_url = reverse_lazy('e_types_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(EquipmentTypeUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EquipmentTypeUpdateView, self).get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context


@login_required
def equipment_type_delete(request, pk):
    if not request.user.is_staff:
        raise Http404
    EquipmentType.objects.get(pk=pk).delete()
    return redirect('e_types_list')


class EquipmentAttributeListView(AccessMixin, ListView):
    model = EquipmentAttribute
    template_name = 'client_app/equipment_attributes_list.html'
    context_object_name = 'equipment_attributes'
    login_url = reverse_lazy('stuff_user_auth')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(EquipmentAttributeListView, self).dispatch(request, *args, **kwargs)


class EquipmentAttributeCreateView(AccessMixin, CreateView):
    model = EquipmentAttribute
    template_name = 'client_app/equipment_attributes_create.html'
    form_class = EquipmentAttributeForms
    success_url = reverse_lazy('e_attrs_list')
    login_url = reverse_lazy('stuff_user_auth')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(EquipmentAttributeCreateView, self).dispatch(request, *args, **kwargs)


@login_required
def delete_equipment_attributes(request, pk):
    if not request.user.is_staff:
        raise Http404
    EquipmentAttribute.objects.get(pk=pk).delete()
    return redirect('e_attrs_list')


class EquipmentAttributeUpdateView(AccessMixin, UpdateView):
    pass


# class EquipmentsListView(AccessMixin, ListView):
#     model = Equipments
#     template_name = 'client_app/equipments_list.html'
#     context_object_name = 'equipments'
#     login_url = reverse_lazy('stuff_user_auth')
#
#     def get_queryset(self):
#         return Equipments.objects.select_related('client').filter(client__slug=self.kwargs['client_slug'])
#
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_staff:
#             raise Http404
#         return super(EquipmentsListView, self).dispatch(request, *args, **kwargs)
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(EquipmentsListView, self).get_context_data(**kwargs)
#         context['client'] = get_object_or_404(Clients, slug=self.kwargs['client_slug'])
#         return context
