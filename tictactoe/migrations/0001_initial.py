# Generated by Django 3.2.6 on 2022-05-29 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TicTacToe',
            fields=[
                ('id_game', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('resultado', models.CharField(choices=[('X', 'El jugador X gano la partida'), ('O', 'El jugador O gano la partida'), ('T', 'La partida acabo en tablas'), ('P', 'La partida sin terminar')], default='P', max_length=1)),
            ],
            options={
                'verbose_name': 'TicTacToe',
            },
        ),
    ]
