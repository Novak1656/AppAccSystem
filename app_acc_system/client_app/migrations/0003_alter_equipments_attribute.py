# Generated by Django 4.1.1 on 2022-10-07 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_app', '0002_alter_clients_inn_alter_clients_kpp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipments',
            name='attribute',
            field=models.ManyToManyField(blank=True, related_name='equipments', to='client_app.equipmentattribute', verbose_name='Атрибуты'),
        ),
    ]