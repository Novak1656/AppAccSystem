import os
import shutil

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from ..forms import ContractsFilesForms, ContractsForms
from ..models import ContractFiles, Contracts, Clients
from ..services import chek_is_staff


class ContractsListView(AccessMixin, ListView):
    model = Contracts
    template_name = 'client_app/contracts_list.html'
    context_object_name = 'contracts'
    login_url = reverse_lazy('stuff_user_auth')

    def get_queryset(self):
        return Contracts.objects.select_related('client').filter(client__slug=self.kwargs['client_slug'])

    def dispatch(self, request, *args, **kwargs):
        chek_is_staff(request.user)
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
        chek_is_staff(request.user)
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
        chek_is_staff(request.user)
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
        chek_is_staff(request.user)
        return super(ContractsUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContractsUpdateView, self).get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context


@login_required
def contracts_delete_view(request, cont_slug):
    chek_is_staff(request.user)
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
        chek_is_staff(request.user)
        return super(ContractFilesCreateView, self).dispatch(request, *args, **kwargs)


@login_required
def delete_cont_file(request, file_slug):
    chek_is_staff(request.user)
    file_obj = get_object_or_404(ContractFiles, slug=file_slug)
    cont_slug = file_obj.contract.slug
    file_obj.delete()
    return redirect('cont_detail', cont_slug=cont_slug)
