# Generated by Django 4.2.2 on 2023-06-18 00:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_evotech', '0027_lieu_produits_artis_photo_produitid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lieu',
            name='produitArtis',
        ),
    ]
