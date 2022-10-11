from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Applications
from client_app.models import Clients
from .forms import ApplicationsForms


class ApplicationsListView(AccessMixin, ListView):
    model = Applications
    template_name = 'main_app/applications_list.html'
    context_object_name = 'applications'
    login_url = reverse_lazy('stuff_user_auth')

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

    def post(self, request, *args, **kwargs):
        pass

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.client = Clients.objects.get(pk=self.request.GET.get('client'))
        self.object.save()
        form.save_m2m()
        return super(ApplicationCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ApplicationCreateView, self).get_context_data(**kwargs)
        context['client'] = Clients.objects.get(pk=self.request.GET.get('client'))
        context['form'] = self.form_class(client_id=self.request.GET.get('client'))
        return context
