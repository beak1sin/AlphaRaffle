"""
ASGI config for AlphaRaffle project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AlphaRaffle.settings')

application = get_asgi_application()


# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import draw.routing   # WebSocket 라우팅 설정 파일

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AlphaRaffle.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             draw.routing.websocket_urlpatterns
#         )
#     ),
# })