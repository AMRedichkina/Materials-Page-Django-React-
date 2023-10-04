"""
    URL patterns for WebSocket consumers.
    
    This list defines the URL patterns for WebSocket consumers. It associates the
    'MaterialStatusConsumer' consumer with the '/ws/material_status/' URL endpoint,
    allowing WebSocket connections for real-time material status updates.
"""

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import MaterialStatusConsumer

websocket_urlpatterns = [
    path('ws/material_status/', MaterialStatusConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns)
})
