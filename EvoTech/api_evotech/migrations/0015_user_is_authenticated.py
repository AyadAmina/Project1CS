# Generated by Django 4.2.1 on 2023-06-17 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_evotech', '0014_remove_user_groups_remove_user_is_superuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_authenticated',
            field=models.BooleanField(default=False),
        ),
    ]
