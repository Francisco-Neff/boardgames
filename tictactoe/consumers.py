import json
from threading import Thread
import concurrent.futures
from multiprocessing.pool import ThreadPool
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import TicTacToe


class TicTacToeConsumer(AsyncJsonWebsocketConsumer):
    id_game=None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['sala']
        self.room_group_name = 'sala_%s' % self.room_name
        
        # Unirse a la sala
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print("Desconectado")
        # Abandono de sala o desconexión.
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """
        Receive mensaje from WebSocket.
        Get the evento and send the appropriate evento
        """
        response = json.loads(text_data)
        evento = response.get("evento", None)
        mensaje = response.get("mensaje", None)
        if evento == 'MOVE':
            # Send mensaje to room group
            ### TODO update del estado del tablero 
            ### Revisar quien empieza siempre si no meter a quien le toca mover
            if mensaje != None:
                thread=Thread(target=TicTacToe.updateTablero,args=(self,mensaje['id_game'],mensaje['ficha'],mensaje['index']))
                thread.start()
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_mensaje',
                'mensaje': mensaje,
                "evento": "MOVE"
            })
            
        if evento == 'START':
            # Send mensaje to room group
            print('inicio partida')
            if mensaje != None:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    thread = executor.submit(TicTacToe.crearSala,mensaje['sala'],mensaje['jugador'],mensaje['ficha'])
                    self.id_game = thread.result()
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_mensaje',
                'mensaje': mensaje,
                'evento': "START"
            })
            
        if evento == 'END':
            # Send mensaje to room group
            ### TODO meter el save final del registro.
            if mensaje != None:
                thread=Thread(target=TicTacToe.cerrarPartida,args=(self,mensaje['id_game'],mensaje['ficha'],mensaje['index'],mensaje['final']))
                thread.start()
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_mensaje',
                'mensaje': mensaje,
                'evento': "END"
            })
         

    async def send_mensaje(self, res):
        """ Receive mensaje from room group """
        # Send mensaje to WebSocket
        if self.id_game != None:
            await self.send(text_data=json.dumps({
                "respuesta": res,
                "id_game": str(self.id_game),
            }))
        else:
            await self.send(text_data=json.dumps({
                "respuesta": res,
            }))