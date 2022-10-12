from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from .models import Applications
from client_app.models import Clients
from .forms import ApplicationsForms
from stuff_app.models import StuffUsers


class ApplicationsListView(AccessMixin, ListView):
    model = Applications
    template_name = 'main_app/applications_list.html'
    context_object_name = 'applications'
    login_url = reverse_lazy('stuff_user_auth')

    def get_queryset(self):
        return Applications.objects.select_related('client', 'contact_person').all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ApplicationsListView, self).get_context_data(**kwargs)
        context['clients'] = Clients.objects.values('pk', 'name').all()
        return context


class ApplicationCreateView(AccessMixin, CreateView):
    model = Applications
    template_name = 'main_app/applications_create.html'
    form_class = ApplicationsForms
    success_url = reverse_lazy('app_list')
    login_url = reverse_lazy('stuff_user_auth')

    def get_form_kwargs(self):
        kwargs = {
            'client_id': self.request.GET.get('client'),
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
            })
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.client = Clients.objects.get(pk=self.request.GET.get('client'))
        self.object.save()
        form.save_m2m()
        return super(ApplicationCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ApplicationCreateView, self).get_context_data(**kwargs)
        context['client'] = Clients.objects.get(pk=self.request.GET.get('client'))
        return context


class ApplicationDetailView(AccessMixin, DetailView):
    model = Applications
    template_name = 'main_app/applications_detail.html'
    context_object_name = 'application'
    login_url = reverse_lazy('stuff_user_auth')
    slug_url_kwarg = 'app_slug'

    def get_queryset(self):
        return Applications.objects.select_related(
            'client', 'contact_person', 'contract'
        ).prefetch_related('equipment').filter(slug=self.kwargs['app_slug'])

    def get_context_data(self, **kwargs):
        context = super(ApplicationDetailView, self).get_context_data(**kwargs)
        context['executors'] = StuffUsers.objects.filter(role='executor').all()
        return context


@login_required
def set_application_executor(request, app_slug):
    application = Applications.objects.get(slug=app_slug)
    executor = StuffUsers.objects.get(pk=request.GET.get('executor'))
    application.executor = executor
    application.save()
    return redirect('app_detail', app_slug=app_slug)
