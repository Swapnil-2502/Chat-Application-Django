"""
ASGI config for ChatApplication project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.urls import path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.consumers import ChatConsumer, OnlineStatusConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatApplication.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": application,
    "websocket" : AuthMiddlewareStack(
        URLRouter([
            path('ws/<int:id>/', ChatConsumer.as_asgi()),
            path('ws/online/', OnlineStatusConsumer.as_asgi())
        ])
   )       
})