import os
import shutil

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from ..forms import EquipmentFilesForm, EquipmentsForms, EquipmentAttributeForms, EquipmentTypeForms
from ..models import EquipmentFiles, Equipments, EquipmentAttribute, EquipmentType, Clients
from ..services import chek_access_rights


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
    model = EquipmentAttribute
    template_name = 'client_app/equipment_attributes_update.html'
    form_class = EquipmentAttributeForms
    success_url = reverse_lazy('e_attrs_list')
    login_url = reverse_lazy('stuff_user_auth')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(EquipmentAttributeUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EquipmentAttributeUpdateView, self).get_context_data(**kwargs)
        context['attr_name'] = self.object.name
        context['form'] = self.form_class(instance=self.object)
        return context


class EquipmentsListView(AccessMixin, ListView):
    model = Equipments
    template_name = 'client_app/equipments_list.html'
    context_object_name = 'equipments'
    login_url = reverse_lazy('stuff_user_auth')

    def get_queryset(self):
        return Equipments.objects.select_related('client', 'type').prefetch_related('attribute')\
            .filter(client__slug=self.kwargs['client_slug'])

    def dispatch(self, request, *args, **kwargs):
        chek_access_rights(request.user)
        return super(EquipmentsListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EquipmentsListView, self).get_context_data(**kwargs)
        context['client'] = get_object_or_404(Clients, slug=self.kwargs['client_slug'])
        return context


class EquipmentsCreateView(AccessMixin, CreateView):
    model = Equipments
    template_name = 'client_app/equipments_create.html'
    form_class = EquipmentsForms
    login_url = reverse_lazy('stuff_user_auth')

    def get_success_url(self):
        return reverse('eq_list', kwargs={'client_slug': self.kwargs['client_slug']})

    def dispatch(self, request, *args, **kwargs):
        chek_access_rights(request.user)
        return super(EquipmentsCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.client = get_object_or_404(Clients, slug=self.kwargs['client_slug'])
        self.object.save()
        self.object.attribute.set(EquipmentAttribute.objects.filter(type_e=self.object.type).all())
        self.object.save()
        return super(EquipmentsCreateView, self).form_valid(form)


class EquipmentsDetailView(AccessMixin, DetailView):
    model = Equipments
    template_name = 'client_app/equipments_detail.html'
    context_object_name = 'equipment'
    login_url = reverse_lazy('stuff_user_auth')
    slug_url_kwarg = 'eq_slug'

    def get_queryset(self):
        return Equipments.objects.filter(slug=self.kwargs['eq_slug']).\
            select_related('type').prefetch_related('attribute', 'files').all()

    def dispatch(self, request, *args, **kwargs):
        chek_access_rights(request.user)
        return super(EquipmentsDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EquipmentsDetailView, self).get_context_data(**kwargs)
        context['eq_files'] = self.object.files.all()
        return context


@login_required
def equipments_delete_view(request, eq_slug):
    chek_access_rights(request.user)
    eq = Equipments.objects.select_related('client').get(slug=eq_slug)
    client_slug = eq.client.slug
    if eq.files.exists():
        files_path = os.path.join(settings.BASE_DIR, f"media/Equipment_files/{eq.name}/")
        shutil.rmtree(files_path)
    eq.delete()
    return redirect('eq_list', client_slug=client_slug)


class EquipmentsUpdateView(AccessMixin, UpdateView):
    model = Equipments
    template_name = 'client_app/equipments_update.html'
    login_url = reverse_lazy('stuff_user_auth')
    slug_url_kwarg = 'eq_slug'
    form_class = EquipmentsForms

    def form_valid(self, form):
        old_data = self.model.objects.values('name', 'type').filter(slug=self.kwargs['eq_slug']).first()
        if self.object.name != old_data.get('name'):
            old_file_path = os.path.join(settings.BASE_DIR, f'media/Equipment_files/{old_data.get("name")}/')
            new_file_path = os.path.join(settings.BASE_DIR, f'media/Equipment_files/{self.object.name}/')
            os.rename(old_file_path, new_file_path)
            files = self.object.files.all()
            for f_obj in files:
                f_obj.file.name = f"Equipment_files/{self.object.name}/{f_obj.filename}"
                f_obj.save()
            self.object.save()
        if self.object.type != EquipmentType.objects.get(pk=old_data.get('type')):
            self.object = form.save(commit=False)
            new_attrs = EquipmentAttribute.objects.filter(type_e=self.object.type).all()
            del_attrs = EquipmentAttribute.objects.filter(~Q(type_e=self.object.type)).all()
            for attr in del_attrs:
                self.object.attribute.remove(attr)
            for attr in new_attrs:
                self.object.attribute.add(attr)
            self.object.save()
        return super(EquipmentsUpdateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        chek_access_rights(request.user)
        return super(EquipmentsUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('eq_detail', kwargs={'eq_slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super(EquipmentsUpdateView, self).get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        context['eq_name'] = self.object.name
        return context


class EquipmentFilesCreateView(AccessMixin, CreateView):
    model = EquipmentFiles
    template_name = 'client_app/equipments_create_file.html'
    form_class = EquipmentFilesForm
    slug_url_kwarg = 'eq_slug'
    login_url = reverse_lazy('stuff_user_auth')

    def get_success_url(self):
        return reverse('eq_detail', kwargs={'eq_slug': self.kwargs['eq_slug']})

    def dispatch(self, request, *args, **kwargs):
        chek_access_rights(request.user)
        return super(EquipmentFilesCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.equipment = get_object_or_404(Equipments, slug=self.kwargs['eq_slug'])
        self.object.save()
        return super(EquipmentFilesCreateView, self).form_valid(form)


@login_required
def delete_eq_file(request, file_slug):
    chek_access_rights(request.user)
    eq_file = EquipmentFiles.objects.select_related('equipment').get(slug=file_slug)
    eq_slug = eq_file.equipment.slug
    eq_file.delete()
    return redirect('eq_detail', eq_slug=eq_slug)
