# Generated by Django 4.1.1 on 2022-09-22 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuff_app', '0004_alter_stuffusers_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='stuffusers',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
