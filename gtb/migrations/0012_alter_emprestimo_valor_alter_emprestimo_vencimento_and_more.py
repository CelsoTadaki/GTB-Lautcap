# Generated by Django 5.0.4 on 2024-04-10 05:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtb', '0011_alter_emprestimo_vencimento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprestimo',
            name='valor',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='emprestimo',
            name='vencimento',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 10, 2, 33, 45, 81095)),
        ),
        migrations.AlterField(
            model_name='historicocompraevendaacoes',
            name='valor',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='historicotransferencias',
            name='valor',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='pessoajuridica',
            name='saldo_da_conta',
            field=models.FloatField(default=0),
        ),
    ]
