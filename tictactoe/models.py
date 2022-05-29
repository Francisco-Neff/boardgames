from django.db import models
from users.models import GameUsers

# Create your models here.


class TicTacToe(models.Model):
    class Resultado_Posibilidades(models.TextChoices):
        ganadorX = 'X' ,'El jugador X gano la partida'
        ganadorO = 'O' ,'El jugador O gano la partida'
        empate = 'T' ,'La partida acabo en tablas'
        proceso =  'P' ,'La partida sin terminar'
    id_game=models.CharField(max_length=7,primary_key=True)
    jugador_X=models.ForeignKey(GameUsers ,related_name="gamertag_X",on_delete=models.SET('Usuario eliminado'))
    jugador_O= models.ForeignKey(GameUsers,related_name="gamertag_O",on_delete=models.SET('Usuario eliminado'))
    resultado=models.CharField(max_length=1,choices=Resultado_Posibilidades.choices, default=Resultado_Posibilidades.proceso)

    class Meta:
        verbose_name='TicTacToe'
        