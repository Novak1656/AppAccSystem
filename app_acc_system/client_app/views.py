from django.contrib.auth.mixins import AccessMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import *
from .forms import ClientForm


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
