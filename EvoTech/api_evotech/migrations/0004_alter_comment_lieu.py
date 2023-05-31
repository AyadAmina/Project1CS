# Generated by Django 4.2.1 on 2023-05-31 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_evotech', '0003_rename_evenement_comment_lieu_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='lieu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api_evotech.lieu'),
        ),
    ]
