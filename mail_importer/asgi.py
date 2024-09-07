import os

import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

django.setup()

import mails.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mail_importer.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            mails.routing.websocket_urlpatterns
        )
    ),
})
