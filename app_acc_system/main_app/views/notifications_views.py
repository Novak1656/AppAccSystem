from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView

from client_app.services import chek_is_staff
from stuff_app.models import StuffUsersNotifications, StuffUsers


class NotificationsSettingsListView(AccessMixin, ListView):
    model = StuffUsers
    template_name = 'main_app/notifications_settings.html'
    context_object_name = 'staffs'
    login_url = reverse_lazy('stuff_user_auth')

    def dispatch(self, request, *args, **kwargs):
        chek_is_staff(request.user)
        return super(NotificationsSettingsListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(notifications_active=True).values(
            'pk', 'first_name', 'second_name', 'last_name', 'role'
        ).order_by('role')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NotificationsSettingsListView, self).get_context_data(**kwargs)
        context['staff_users'] = StuffUsers.objects.filter(notifications_active=False)
        return context


@login_required
def turn_on_staff_notifications(request):
    stuffs = request.GET.getlist('stuff')
    stuffs_queryset = StuffUsers.objects.filter(pk__in=stuffs)
    for stuff_obj in stuffs_queryset:
        stuff_obj.notifications_active = True
    StuffUsers.objects.bulk_update(stuffs_queryset, ['notifications_active'])
    return redirect('notifications_settings')


@login_required
def turn_off_staff_notifications(request):
    StuffUsers.objects.filter(pk=request.GET.get('stuff_pk')).update(notifications_active=False)
    return redirect('notifications_settings')


@login_required
def delete_notification(request):
    StuffUsersNotifications.objects.get(pk=request.GET.get('notify_pk')).delete()
    return redirect(request.META['HTTP_REFERER'])


@login_required
def notification_is_viewed(request):
    StuffUsersNotifications.objects.filter(pk=request.GET.get('notify_pk')).update(is_viewed=True)
    return redirect(request.META['HTTP_REFERER'])
