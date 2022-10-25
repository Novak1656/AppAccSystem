from django.template import Library

register = Library()


@register.filter(name='role_normalize')
def role_normalize(role):
    roles = {'admin': 'Администратор', 'dispatcher': 'Диспетчер', 'executor': 'Исполнитель'}
    return roles.get(role)


@register.inclusion_tag('')
def get_user_notifications():
    context = dict()

    return context
