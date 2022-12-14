# Generated by Django 4.1.1 on 2022-10-11 20:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0002_alter_commentsfiles_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applications',
            name='closing_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата закрытия'),
        ),
        migrations.AlterField(
            model_name='applications',
            name='executor',
            field=models.ForeignKey(blank=True, help_text='Выберите исполнителя...', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='applications', to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель'),
        ),
    ]
