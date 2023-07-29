from django.urls import path
from draw import consumers

websocket_urlpatterns = [
    path('ws/notification/', consumers.NotificationConsumer.as_asgi()),
    # 여기에 WebSocket 연결에 대한 URL 패턴을 추가할 수 있습니다.
]