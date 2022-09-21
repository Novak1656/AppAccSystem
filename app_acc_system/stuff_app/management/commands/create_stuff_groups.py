from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Создание группы пользователей для сотрудников'

    def handle(self, *args, **options):
        groups_name = ['admin', 'dispatcher', 'executor']
        for g_name in groups_name:
            new_group, created = Group.objects.get_or_create(name=g_name)
            # ct = ContentType.objects.get_for_model(Project)
            # permission = Permission.objects.create(codename='can_add_project',
            #                                        name='Can add project',
            #                                        content_type=ct)
            # new_group.permissions.add(permission)
        self.stdout.write(self.style.SUCCESS('Создание группы пользователей для сотрудников прошло успешно'))
