# Generated by Django 5.0.4 on 2024-04-10 22:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtb', '0013_historicocompraevendaacoes_user_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pessoafisica',
            name='user_acoes',
        ),
        migrations.AlterField(
            model_name='emprestimo',
            name='vencimento',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 10, 19, 1, 40, 591491)),
        ),
    ]
