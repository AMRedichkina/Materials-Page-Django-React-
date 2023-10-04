"""
    ASGI application configuration for handling HTTP and WebSocket connections.
    
    the ASGI application configuration is set up for handling both HTTP and WebSocket
    connections, specifically for updating materials in real-time.

    This configuration sets up the ASGI application to handle both HTTP and WebSocket
    connections. It uses the get_asgi_application() function to handle HTTP connections
    and the URLRouter with WebSocket URL patterns to handle WebSocket connections.
    
    Attributes:
        "http" (ASGIApplication): ASGI application for handling HTTP connections.
        "websocket" (URLRouter): URLRouter for handling WebSocket connections.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import materials_project.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'materials_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(materials_project.routing.websocket_urlpatterns),
})
