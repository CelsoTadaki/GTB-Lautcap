# Generated by Django 5.0.4 on 2024-04-10 02:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtb', '0005_alter_emprestimo_vencimento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicocompraevendaacoes',
            name='tipo',
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='dias_ate_vencimento',
            field=models.IntegerField(default=30),
        ),
        migrations.AddField(
            model_name='pessoafisica',
            name='userAcoes',
            field=models.ManyToManyField(related_name='acoes', to='gtb.historicocompraevendaacoes'),
        ),
        migrations.AlterField(
            model_name='emprestimo',
            name='vencimento',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 9, 23, 41, 54, 567956)),
        ),
    ]