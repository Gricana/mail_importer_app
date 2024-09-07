import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

from .imap_utils import get_emails

logger = logging.getLogger(__name__)


class EmailConsumer(AsyncWebsocketConsumer):
    """
    This class represents a WebSocket consumer for handling email-related operations.
    """

    async def connect(self):
        """
        This method is called when a WebSocket connection is established.
        It adds the consumer to a group named 'mails_group' and logs the connection event.
        """
        self.group_name = 'mails_group'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        logger.info(f"User {self.scope['user']} connected")
        await self.accept()

    async def disconnect(self, close_code):
        """
        This method is called when a WebSocket connection is closed.
        It removes the consumer from the 'mails_group' and logs the disconnection event.
        """
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )
        logger.info(f"User {self.scope['user']} disconnected with code {close_code}")

    async def receive(self, text_data=None, bytes_data=None):
        """
        This method is called when a message is received over the WebSocket.
        It processes the received data and performs email-related operations.
        """
        try:
            data = json.loads(text_data)
            user = self.scope["user"]

            if user.is_authenticated and data.get('type') == 'import':
                await get_emails(user, self)
            else:
                await self.send(text_data=json.dumps({
                    'error': 'User not authenticated'
                }))
        except Exception as e:
            logger.error(f"Error in receive: {e}")
            await self.send(text_data=json.dumps({
                'error': 'An error occurred'
            }))

    async def send_progress(self, progress, message):
        """
        This method sends a progress update message over the WebSocket.
        """
        await self.send(text_data=json.dumps({
            'type': 'progress',
            'progress': progress,
            'message': message
        }))

    async def send_message(self, message):
        """
        This method sends a message over the WebSocket.
        It takes a message as a parameter and sends it as a JSON object.
        """
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': message
        }))
