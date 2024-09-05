import json

from channels.generic.websocket import AsyncWebsocketConsumer

from .imap_utils import get_emails


class EmailConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'mails_group'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        email = data['email']
        password = data['password']

        await get_emails(email, password, self)

    async def send_progress(self, progress, message=None):
        await self.send(text_data=json.dumps({
            'progress': progress,
            'message': message
        }))

    async def send_message(self, message_data):
        await self.send(text_data=json.dumps({
            'new_message': message_data
        }))
