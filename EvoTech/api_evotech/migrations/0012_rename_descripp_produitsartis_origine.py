# Generated by Django 4.2.1 on 2023-06-16 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_evotech', '0011_photo_produitid_produitsartis_descripp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='produitsartis',
            old_name='descripP',
            new_name='origine',
        ),
    ]
