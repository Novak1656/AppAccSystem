# Generated by Django 4.1.1 on 2022-09-21 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuff_app', '0003_alter_stuffusers_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stuffusers',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Отчество'),
        ),
    ]