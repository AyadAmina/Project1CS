# Generated by Django 4.1.3 on 2023-06-15 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_evotech', '0004_historylieu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historylieu',
            name='Idlieu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_evotech.lieu'),
        ),
    ]