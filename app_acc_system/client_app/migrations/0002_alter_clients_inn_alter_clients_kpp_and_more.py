# Generated by Django 4.1.1 on 2022-09-27 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='inn',
            field=models.CharField(help_text='Пример: 0000000000', max_length=10, unique=True, verbose_name='ИНН'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='kpp',
            field=models.CharField(help_text='Пример: 000000000', max_length=9, unique=True, verbose_name='КПП'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='ogrn',
            field=models.CharField(help_text='Пример: 0000000000000', max_length=13, unique=True, verbose_name='ОГРН'),
        ),
    ]
