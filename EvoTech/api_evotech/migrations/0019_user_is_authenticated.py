# Generated by Django 4.2.2 on 2023-06-17 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_evotech', '0018_search'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_authenticated',
            field=models.BooleanField(default=False),
        ),
    ]
