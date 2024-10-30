from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json


class EmailConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'email_progress'
        self.room_group_name = 'email_progress_group'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Начать получение электронных писем здесь и отправить обновления в WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'email_progress',
                'message': message,
            }
        )

    async def email_progress(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message,
        }))
