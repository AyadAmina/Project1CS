# Generated by Django 4.1.4 on 2023-05-29 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('idCategorie', models.AutoField(default='', primary_key=True, serialize=False)),
                ('labelC', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Evenement',
            fields=[
                ('idEvent', models.AutoField(primary_key=True, serialize=False)),
                ('nomEvent', models.CharField(max_length=100)),
                ('descripEvent', models.CharField(max_length=1000)),
                ('dateEvent', models.DateField()),
                ('H_debut', models.TimeField()),
                ('H_fin', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Lieu',
            fields=[
                ('idLieu', models.AutoField(primary_key=True, serialize=False)),
                ('nomLieu', models.CharField(max_length=100)),
                ('descripLieu', models.CharField(max_length=1000)),
                ('exigence', models.CharField(max_length=1000)),
                ('faitHisto', models.CharField(max_length=1000)),
                ('produitArtis', models.CharField(default='', max_length=1000)),
                ('expressCourantes', models.CharField(max_length=1000)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('H_ouverture', models.TimeField()),
                ('H_fermeture', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Meteo',
            fields=[
                ('idMeteo', models.AutoField(primary_key=True, serialize=False)),
                ('Temperature', models.IntegerField()),
                ('prevision', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MoyenTransport',
            fields=[
                ('idTransport', models.AutoField(primary_key=True, serialize=False)),
                ('typeTrans', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('numRegion', models.AutoField(primary_key=True, serialize=False)),
                ('nomRegion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('idTheme', models.AutoField(primary_key=True, serialize=False)),
                ('labelT', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('idUser', models.AutoField(primary_key=True, serialize=False)),
                ('nomUser', models.CharField(max_length=100)),
                ('prenomUser', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('motdepasse', models.CharField(max_length=100)),
                ('profile', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ville',
            fields=[
                ('idVille', models.AutoField(primary_key=True, serialize=False)),
                ('nomVille', models.CharField(max_length=100)),
                ('regionV', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_evotech.region')),
            ],
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id_trans', models.AutoField(primary_key=True, serialize=False)),
                ('H_depart', models.TimeField()),
                ('id_lieu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_evotech.lieu')),
                ('id_moytrans', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_evotech.moyentransport')),
            ],
        ),
        migrations.CreateModel(
            name='Favoris',
            fields=[
                ('id_favoris', models.AutoField(primary_key=True, serialize=False)),
                ('idUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_evotech.user')),
                ('id_lieu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_evotech.lieu')),
            ],
        ),
        migrations.AddField(
            model_name='region',
            name='adminRegion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_evotech.user'),
        ),
        migrations.AddField(
            model_name='lieu',
            name='adminRegion',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api_evotech.user'),
        ),
        migrations.AddField(
            model_name='lieu',
            name='climat',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api_evotech.meteo'),
        ),
        migrations.AddField(
            model_name='lieu',
            name='id_event',
            field=models.ManyToManyField(default='', to='api_evotech.evenement'),
        ),
        migrations.AddField(
            model_name='lieu',
            name='region',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api_evotech.region'),
        ),
    ]
