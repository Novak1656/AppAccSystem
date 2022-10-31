import os
import shutil

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.timezone import now
from django.views.generic import ListView, CreateView

from client_app.models import Clients
from main_app.forms import ApplicationsForms, ApplicationCommentsForms
from main_app.models import Applications, ApplicationComments
from main_app.services import new_application_notification, new_comment_notification, \
    new_executor_application_notification, application_status_change_notification
from stuff_app.models import StuffUsers

# Поработать с правами доступа (исполнитель может видеть приватные комменты только для своих заявок)
class ApplicationsListView(AccessMixin, ListView):
    model = Applications
    template_name = 'main_app/applications_list.html'
    context_object_name = 'applications'
    login_url = reverse_lazy('stuff_user_auth')

    def get_queryset(self):
        return Applications.objects.select_related('client', 'contact_person', 'executor').all()

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
        new_application_notification(self.object)
        return super(ApplicationCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ApplicationCreateView, self).get_context_data(**kwargs)
        context['client'] = Clients.objects.get(pk=self.request.GET.get('client'))
        return context


class ApplicationDetailView(AccessMixin, CreateView):
    model = Applications
    template_name = 'main_app/applications_detail.html'
    login_url = reverse_lazy('stuff_user_auth')
    slug_url_kwarg = 'app_slug'
    form_class = ApplicationCommentsForms

    def get_success_url(self):
        return reverse('app_detail', kwargs={'app_slug': self.kwargs['app_slug']})

    def form_valid(self, form):
        application_obj = self.get_context_data().get('application')
        self.object = form.save(commit=False)
        self.object.application = application_obj
        self.object.save()
        new_comment_notification(application_obj, self.object.comment_body, self.object.is_public)
        return super(ApplicationDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ApplicationDetailView, self).get_context_data(**kwargs)
        context['executors'] = StuffUsers.objects.filter(role='executor').all()
        context['application'] = Applications.objects.select_related(
            'client', 'contact_person', 'contract', 'executor'
        ).prefetch_related('equipment', 'comments').get(slug=self.kwargs['app_slug'])
        status_list = {
            'New': [('At work', 'В работе'), ('Postponed', 'Отложена')],
            'At work': [('Postponed', 'Отложена'), ('Solved', 'Решена')],
            'Postponed': [('At work', 'В работе'), ('Solved', 'Решена')],
            'Solved': [('At work', 'В работе'), ('Postponed', 'Отложена'), ('Closed', 'Закрыта')],
        }
        context['status_list'] = status_list.get(context['application'].status)
        return context


@login_required
def set_application_executor(request, app_slug):
    application = Applications.objects.get(slug=app_slug)
    executor = StuffUsers.objects.get(pk=request.GET.get('executor'))
    application.executor = executor
    application.save()
    new_executor_application_notification(application)
    return redirect('app_detail', app_slug=app_slug)


@login_required
def update_comment_body(request, comment_pk):
    ApplicationComments.objects.filter(pk=comment_pk).update(comment_body=request.POST[f'comment_body{comment_pk}'])
    return redirect(request.META['HTTP_REFERER'])


@login_required
def delete_comment(request, comment_pk):
    ApplicationComments.objects.get(pk=comment_pk).delete()
    return redirect(request.META['HTTP_REFERER'])


@login_required
def delete_application(request, app_slug):
    application = Applications.objects.prefetch_related('comments').get(slug=app_slug)
    if application.comments.all().filter(~Q(file=None)).exists():
        files_path = os.path.join(settings.BASE_DIR, f"media/Comment_files/{application.subject}/")
        shutil.rmtree(files_path)
    application.delete()
    return redirect('app_list')


@login_required
def change_application_status(request, app_slug):
    status = request.GET.get('status')
    application = Applications.objects.get(slug=app_slug)
    application.status = status
    if status == 'Closed':
        application.closing_date = now()
    application.save()
    application_status_change_notification(application)
    return redirect('app_detail', app_slug=app_slug)
