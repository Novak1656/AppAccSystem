from django.template import Library
from ..models import Applications

register = Library()


@register.filter(name='status_application_translate')
def status_application_translate(status_value: str) -> str:
    status_list = Applications.STATUS_LIST
    for key, value in status_list:
        if key == status_value:
            return value


@register.filter(name='priority_application_translate')
def priority_application_translate(priority_value: str) -> str:
    priority_list = Applications.PRIORITY_LIST
    for key, value in priority_list:
        if key == priority_value:
            return value


@register.filter(name='type_application_translate')
def type_application_translate(type_value: str) -> str:
    type_list = Applications.TYPE_LIST
    for key, value in type_list:
        if key == type_value:
            return value
