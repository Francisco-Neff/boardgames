from django.conf.urls import url

from .consumers import TicTacToeConsumer

websocket_urlpatterns = [
    url(r'^ttt/partida/(?P<sala>\w+)/$', TicTacToeConsumer.as_asgi()),
]