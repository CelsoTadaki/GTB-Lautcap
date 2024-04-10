# Generated by Django 5.0.4 on 2024-04-10 03:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtb', '0006_remove_historicocompraevendaacoes_tipo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicocompraevendaacoes',
            name='comprador',
        ),
        migrations.AlterField(
            model_name='emprestimo',
            name='vencimento',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 10, 0, 4, 54, 578312)),
        ),
        migrations.AlterField(
            model_name='historicocompraevendaacoes',
            name='quantidade',
            field=models.IntegerField(default=0),
        ),
    ]