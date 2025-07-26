"""
ASGI config for NuxTest project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import game.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NuxTest.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        # WebSocket routing will be wired later when game app is implemented
        "websocket": AuthMiddlewareStack(
            URLRouter(game.routing.websocket_urlpatterns),
        ),
    }
)
