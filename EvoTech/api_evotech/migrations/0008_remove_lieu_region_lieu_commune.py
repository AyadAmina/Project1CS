# Generated by Django 4.1.5 on 2023-05-27 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_evotech', '0007_rename_ville_commune_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lieu',
            name='region',
        ),
        migrations.AddField(
            model_name='lieu',
            name='commune',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api_evotech.commune'),
        ),
    ]
