import uuid
from django.db import models
from django.db.models import Q
from django.core.validators import MaxValueValidator
from django.forms import NullBooleanField
from pymysql import NULL
from users.models import GameUsers

# Create your models here.


class TicTacToe(models.Model):
    class Resultado_Posibilidades(models.TextChoices):
        ganadorX = 'X' ,'El jugador X gano la partida'
        ganadorO = 'O' ,'El jugador O gano la partida'
        empate =  'T' ,'La partida acabo en tablas'
        proceso =  'P' ,'La partida sigue en curso'
        inciada = 'I', 'La partida la ha iniciado un jugador, a la espera del rival.'
        abandono = 'D', 'Un jugador se ha desconectado, a la espera de que vuelva.'
    id_game=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,serialize=True)
    sala_cod=models.PositiveIntegerField(unique=False,validators=[MaxValueValidator(9999)])
    jugador_X=models.ForeignKey(GameUsers,related_name="gamertag_X",on_delete=models.SET('Usuario eliminado'),null=True)
    jugador_O= models.ForeignKey(GameUsers,related_name="gamertag_O",on_delete=models.SET('Usuario eliminado'),null=True)
    tablero=models.CharField(max_length=100,default=0)
    resultado=models.CharField(max_length=1,choices=Resultado_Posibilidades.choices, default=Resultado_Posibilidades.inciada)

    class Meta:
        verbose_name='TicTacToe'

    @classmethod
    def crearSala(self,sala_cod,username,ficha):
        """
        Este método crea el registro en BBDD de la sala a través del evento START.
        TODO
        Además si el cliente ha sufrido una reconexión|caída comprueba el estado o si tiene una partida pendiente 
        para devolver los datos de esta y continuar por donde se quedo.
        """
        ### TODO meter el reconect
        #Para cada Sala iniciada (resultado=I) se hace el update de la sala con el nuevo jugador y se devuelve el id de esta.
        id_game = None
        salas_iniciadas = TicTacToe.objects.filter(Q(sala_cod=sala_cod) & Q(resultado=TicTacToe.Resultado_Posibilidades.inciada))
        for sala in salas_iniciadas:
            if int(sala_cod) == getattr(sala,'sala_cod'): 
                print('update')
                id_game = self.updateSala(self,getattr(sala,'id_game'),username,ficha)

        # Si no existe ninguna sala iniciada o empezada se crea un nuevo registro.
        if id_game==None:
            reg = TicTacToe()
            print('nuevo registro')
            reg.sala_cod = sala_cod
            if ficha == 'X':
                reg.jugador_X = GameUsers.objects.get(username=username)
            elif ficha == 'O':
                reg.jugador_O = GameUsers.objects.get(username=username)
            else:
                print('Opción no valida')
                return -1
            reg.save()
            id_game = reg.id_game
        return id_game

    def updateSala(self,id_game,username,ficha):
        """
        Este método actualiza el registro en BBDD de la sala a través del evento START., con el segundo jugador.
        """
        reg = TicTacToe.objects.get(id_game=id_game)
        reg.resultado=TicTacToe.Resultado_Posibilidades.proceso
        if ficha == 'X':
            reg.jugador_X = GameUsers.objects.get(username=username)
        elif ficha == 'O':
            reg.jugador_O = GameUsers.objects.get(username=username)
        else:
            print('Opción no valida')
            return None
        reg.save()
        return reg.id_game
    
    def updateTablero(self,id_game,ficha,movimiento):
        """
        Este método actualiza el tablero de la sala ya creada, se actualiza cada vez que uno de los dos jugadores hace un movimiento,
        se invoca tras lanzar el evento MOVE durante la partida.
        Se ingresa la ficha que hace el movimiento y el indice de donde ha colocado su ficha. 
        """
        reg = TicTacToe.objects.get(id_game=id_game)
        act = str(ficha)+':'+str(movimiento)
        if len(reg.tablero)>1:
            if not act in reg.tablero:
                reg.tablero = reg.tablero +', '+ act
        else:
            reg.tablero =  act
        reg.save()
    
    def cerrarPartida(self,id_game,ficha,movimiento,final):
        """
        El ganador de la partida sera el de la variable ficha, a no ser que la partida haya quedado empate, por lo que final = T.
        """
        #Revisar si se guarda el movimiento final
        reg = TicTacToe.objects.get(id_game=id_game)
        print('partida finalizada')
        if final != 'T':
            if ficha == 'X':
                jug=GameUsers.objects.get(username=reg.jugador_X.username)
            elif ficha == 'O':
                jug=GameUsers.objects.get(username=reg.jugador_O.username)
            jug.ganadas += 1
            jug.save()
            reg.resultado = ficha     
        else:
            reg.resultado = TicTacToe.Resultado_Posibilidades.empate
        reg.save()
    
    def discPartida(self,id_game):
        """
        Uno de los jugadores a sufrido una desconexión durante la partida o la ha abandonado. A partir de ahora la partida no sera en tiempo real si no 
        que se tendrá que buscar a través de views.partidasPendientes.
        Si el resultado de la partida es 'I' o alguno de los dos jugadores en None esta se borrara por solo tener un jugador activo.
        """
        reg = TicTacToe.objects.get(id_game=id_game)
        print(reg.jugador_O)
        if reg.resultado == TicTacToe.Resultado_Posibilidades.inciada or reg.jugador_X == None or reg.jugador_O == None:
            reg.delete()
        else:    
            reg.resultado = TicTacToe.Resultado_Posibilidades.abandono
            reg.save()

    def partidaslog(id_user):
        """
        Se encuentra el log de todas las partidas ganadas y perdidas por el jugador
        """
        ganadas = TicTacToe.objects.filter((Q(jugador_X=id_user) & Q(resultado='X')) | (Q(jugador_O=id_user) & Q(resultado='O')))
        perdidas = TicTacToe.objects.filter((Q(jugador_X=id_user) & (Q(resultado='O')|Q(resultado='T'))) | (Q(jugador_O=id_user) & (Q(resultado='X')|Q(resultado='T'))))
        return ganadas, perdidas

    

        

