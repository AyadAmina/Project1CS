# Generated by Django 4.2.1 on 2023-06-17 00:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_evotech', '0012_alter_lieu_feedback_alter_lieu_nmb_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historyevent',
            name='Idevent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api_evotech.evenement'),
        ),
        migrations.AlterField(
            model_name='historyevent',
            name='Iduser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api_evotech.user'),
        ),
        migrations.AlterField(
            model_name='historylieu',
            name='Idlieu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api_evotech.lieu'),
        ),
        migrations.AlterField(
            model_name='historylieu',
            name='Iduser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api_evotech.user'),
        ),
        migrations.AlterField(
            model_name='lieu',
            name='categorie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api_evotech.categorie'),
        ),
        migrations.AlterField(
            model_name='lieu',
            name='theme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api_evotech.theme'),
        ),
        migrations.AlterField(
            model_name='region',
            name='adminRegion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api_evotech.user'),
        ),
    ]
