"""
ASGI config for DolarWebApp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator,OriginValidator
from django.urls import path
from polls.consumers import CrawPredictConsume
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DolarWebApp.settings')
from channels.sessions import SessionMiddlewareStack
application = ProtocolTypeRouter({
    "websocket":AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                path('wscrawpredict', CrawPredictConsume.as_asgi(),name="wscraw")
                ]
            )
        )
    )
    # Just HTTP for now. (We can add other protocols later.)
})



