# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # WebSocket 연결 시 실행될 로직
#         print('websocket 연결')
#         await self.accept()

#     async def disconnect(self, close_code):
#         # WebSocket 연결 종료 시 실행될 로직
#         print('websocket 종료')
#         pass

#     async def receive(self, text_data):
#         # WebSocket으로부터 데이터를 받았을 때 실행될 로직
#         pass

#     async def send_notification(self, event):
#         # WebSocket으로 알림을 전송하는 함수
#         print('알림 전송')
#         notification = event['notification']
#         await self.send(text_data=json.dumps(notification))