from django.template import Library

from ..models import StuffUsersNotifications

register = Library()


@register.filter(name='role_normalize')
def role_normalize(role):
    roles = {'admin': 'Администратор', 'dispatcher': 'Диспетчер', 'executor': 'Исполнитель'}
    return roles.get(role)


@register.inclusion_tag('stuff_app/user_notifications.html')
def get_user_notifications(user_obj):
    notifications = StuffUsersNotifications.objects.filter(user=user_obj)
    new_notify_cnt = notifications.filter(is_viewed=False).count()
    context = dict(notifications=notifications, new_notify_cnt=new_notify_cnt)
    return context
