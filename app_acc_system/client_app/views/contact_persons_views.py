from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from ..forms import ContactPersonsForms
from ..models import ContactPersons, Clients
from ..services import chek_access_rights


class ContactPersonsListView(AccessMixin, ListView):
    model = ContactPersons
    template_name = 'client_app/contact_persons_list.html'
    login_url = reverse_lazy('stuff_user_auth')
    context_object_name = 'contact_persons'

    def dispatch(self, request, *args, **kwargs):
        chek_access_rights(request.user)
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
        chek_access_rights(request.user)
        return super(ContactPersonCreateView, self).dispatch(request, *args, **kwargs)


class ContactPersonDetailView(AccessMixin, DetailView):
    model = ContactPersons
    template_name = 'client_app/contact_persons_detail.html'
    context_object_name = 'contact_person'
    login_url = reverse_lazy('stuff_user_auth')

    def dispatch(self, request, *args, **kwargs):
        chek_access_rights(request.user)
        return super(ContactPersonDetailView, self).dispatch(request, *args, **kwargs)


class ContactPersonUpdateView(AccessMixin, UpdateView):
    model = ContactPersons
    template_name = 'client_app/contact_persons_update.html'
    login_url = reverse_lazy('stuff_user_auth')
    form_class = ContactPersonsForms

    def get_success_url(self):
        return reverse_lazy('cp_detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        chek_access_rights(request.user)
        return super(ContactPersonUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContactPersonUpdateView, self).get_context_data(**kwargs)
        context['cp_name'] = self.object.get_full_name
        context['form'] = self.form_class(instance=self.object)
        return context


@login_required
def contact_person_delete(request, cp_pk):
    chek_access_rights(request.user)
    cp_obj = ContactPersons.objects.get(pk=cp_pk)
    client_slug = cp_obj.client.slug
    cp_obj.delete()
    return redirect('cp_list', client_slug=client_slug)
