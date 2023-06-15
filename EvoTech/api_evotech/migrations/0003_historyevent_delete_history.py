# Generated by Django 4.1.3 on 2023-06-15 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_evotech', '0002_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryEvent',
            fields=[
                ('idHis', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('Type_Action', models.CharField(choices=[('Ajout Evenemen', 'Ajout Evenement'), ('Modification Evenement', 'Modification Evenement'), ('Suppression Evenement', 'Suppression Evenement'), ('Ajout lieu', 'Ajout lieu'), ('Modification lieu', 'Modification lieu'), ('Suppression lieu', 'Suppression lieu')], max_length=100)),
                ('Idevent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_evotech.evenement')),
                ('Iduser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_evotech.user')),
            ],
        ),
        migrations.DeleteModel(
            name='History',
        ),
    ]
