"""
ASGI config for boardgames project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import tictactoe.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boardgames.settings')

#application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            tictactoe.routing.websocket_urlpatterns
        )
    ),
})


