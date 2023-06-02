# Generated by Django 4.2.1 on 2023-06-01 23:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_evotech', '0004_alter_comment_lieu'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('comment', models.CharField(max_length=1000)),
                ('lieu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='api_evotech.lieu')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_evotech.user')),
            ],
        ),
    ]
