import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import mails.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourproject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            mails.routing.websocket_urlpatterns
        )
    ),
})
