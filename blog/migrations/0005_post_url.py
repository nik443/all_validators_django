# Generated by Django 3.1 on 2023-11-26 23:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='url',
            field=models.CharField(max_length=50, null=True, validators=[django.core.validators.URLValidator(message='Введите корректный URL', schemes=['sttps'])], verbose_name='url'),
        ),
    ]
