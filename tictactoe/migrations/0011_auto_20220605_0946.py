# Generated by Django 3.1.14 on 2022-06-05 07:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tictactoe', '0010_auto_20220605_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tictactoe',
            name='jugador_O',
            field=models.ForeignKey(null=True, on_delete=models.SET('Usuario eliminado'), related_name='gamertag_O', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tictactoe',
            name='jugador_X',
            field=models.ForeignKey(null=True, on_delete=models.SET('Usuario eliminado'), related_name='gamertag_X', to=settings.AUTH_USER_MODEL),
        ),
    ]
