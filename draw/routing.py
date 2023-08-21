from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/<str:some_room>/', ChatConsumer.as_asgi()),
    path('ws/auth/<str:some_room>/', ChatConsumer.as_asgi()),
    path('ws/auth/details/<str:some_room>/', ChatConsumer.as_asgi()),
    # 여기에 WebSocket 연결에 대한 URL 패턴을 추가할 수 있습니다.
]