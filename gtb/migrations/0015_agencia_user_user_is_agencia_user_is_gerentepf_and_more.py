# Generated by Django 5.0.4 on 2024-04-10 23:51

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtb', '0014_remove_pessoafisica_user_acoes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='agencia',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='is_Agencia',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_gerentePF',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='emprestimo',
            name='vencimento',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 10, 20, 51, 50, 813076)),
        ),
    ]
