# Generated by Django 4.1.1 on 2022-10-11 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_applications_closing_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applications',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дедлайн'),
        ),
    ]