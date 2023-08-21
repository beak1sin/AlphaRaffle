"""
ASGI config for AlphaRaffle project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AlphaRaffle.settings')

# application = get_asgi_application()


import os
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import draw.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AlphaRaffle.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(
        URLRouter(
            draw.routing.websocket_urlpatterns
        ))
    ),
})