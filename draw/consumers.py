import json
from channels.generic.websocket import AsyncWebsocketConsumer
from draw.models import Shoe, Member, Shoeimg, Shoesite, Shoesiteimg, Comment, SearchTerm


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        some_room = self.scope['url_route']['kwargs']['some_room']
        print(self.scope)
        try:
            self.user = self.scope['session']['member_no']
        except:
            self.user = None
        if self.user != None:
            self.group_name = f'user_{self.user}'
            await self.channel_layer.group_add(self.group_name, self.channel_name)
        # self.some_room = some_room
        # self.room_group_name = f'stats-{some_room}'
        # await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # WebSocket 연결 시 실행될 로직
        print('websocket 연결')
        await self.accept()

    async def disconnect(self, close_code):
        # WebSocket 연결 종료 시 실행될 로직
        print(f'websocket 연결 종료: {close_code}')
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # WebSocket으로부터 데이터를 받았을 때 실행될 로직
        text_data_json = json.loads(text_data)
        try:
            message = text_data_json['message']
        except:
            pass
        try:
            sender = text_data_json['sender']
        except:
            pass
        try:
            receiver = text_data_json['receiver']
            receive_member = Member.objects.get(member_nickname = receiver)
            # await self.channel_layer.send(receiver, {
            #     'type': 'statistics_message',
            #     'message': message,
            #     'sender': sender
            # })
            receiver_group_name = f'user_{receive_member.member_no}'
            await self.channel_layer.group_send(receiver_group_name, {
                'type': 'statistics_message',
                'message': message,
                'sender': sender
            })

        except Exception as e:
            print(f'error code: {e}')
        
        # if receiver:
        #     try:
        #         receive_member = Member.objects.get(member_nickname=receiver)
        #         if receive_member.channel_name:
        #             await self.channel_layer.send(receive_member.channel_name, {
        #                 'type': 'send_message',
        #                 'message': message,
        #                 'sender': sender
        #             })
        #         return
        #     except Member.DoesNotExist:
        #         pass

        # await self.channel_layer.group_send(self.room_group_name, {
        #         'type': 'statistics_message',
        #         'message': message,
        #         'sender': sender
        #     })
        # await self.channel_layer.send(receive_member.channel_name, {
        #         'type': 'statistics_message',
        #         'message': message,
        #         'sender': sender
        #     })

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    async def statistics_message(self, event):
        # WebSocket으로 알림을 전송하는 함수
        print('알림 전송')
        message = event['message']
        sender = event['sender']
        await self.send(text_data=json.dumps({'message': message, 'sender': sender }))