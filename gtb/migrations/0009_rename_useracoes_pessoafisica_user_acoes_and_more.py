# Generated by Django 5.0.4 on 2024-04-10 03:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtb', '0008_alter_emprestimo_vencimento'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pessoafisica',
            old_name='userAcoes',
            new_name='user_acoes',
        ),
        migrations.AlterField(
            model_name='emprestimo',
            name='vencimento',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 10, 0, 15, 32, 312822)),
        ),
    ]
