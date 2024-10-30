# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from message import routing as email_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'email_importer.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            email_routing.websocket_urlpatterns
        )
    ),
})