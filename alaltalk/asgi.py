"""
ASGI config for alaltalk project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
from django.core.asgi import get_asgi_application

from apps.chat.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alaltalk.settings.dev")
django.setup()

# chat.router를 root router로 설정
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": SessionMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
