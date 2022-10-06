from django.template import Library
from ..models import EquipmentType, EquipmentAttribute

register = Library()


@register.simple_tag()
def get_e_types_count():
    return EquipmentType.objects.all().count()


@register.simple_tag()
def get_e_attrs_count():
    return EquipmentAttribute.objects.all().count()
