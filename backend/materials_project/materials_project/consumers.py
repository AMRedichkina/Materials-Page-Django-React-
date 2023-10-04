from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MaterialStatusConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time material status updates.
    
    This consumer handles WebSocket connections for receiving real-time updates
    about material status changes. It allows clients to subscribe to the 'material_status'
    group and receive updates when new materials are added or existing materials are updated.
    
    Methods:
        connect(): Called when a WebSocket connection is established.
        disconnect(close_code): Called when a WebSocket connection is closed.
        receive(text_data): Called when data is received over the WebSocket connection.
        update_material_status(event): Sends material status updates to connected clients.
        new_material(event): Sends notifications about new materials to connected clients.
    """

    async def connect(self):
        """
        Called when a WebSocket connection is established.
        """
        print("Trying to connect...")
        await self.channel_layer.group_add(
            "material_status",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """
        Called when a WebSocket connection is closed.
        """
        await self.channel_layer.group_discard(
            "material_status",
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    async def update_material_status(self, event):
        """
        Sends material status updates to connected clients.

        Args:
            event (dict): Event data containing material status updates.
        """
        await self.send(text_data=json.dumps(event))
    
    async def new_material(self, event):
        """
        Sends notifications about new materials to connected clients.

        Args:
            event (dict): Event data containing information about new materials.
        """
        await self.send(text_data=json.dumps(event))
