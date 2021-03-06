# Generated by Django 3.1.14 on 2022-06-05 07:31

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tictactoe', '0006_auto_20220605_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tictactoe',
            name='tablero_O',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=-1, max_length=6, size=None),
        ),
        migrations.AlterField(
            model_name='tictactoe',
            name='tablero_X',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=-1, max_length=6, size=None),
        ),
    ]
