import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BoxConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "boxes_updates"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Aquí puedes manejar mensajes que vengan desde el cliente si quieres
        # Por ejemplo reenviarlos al grupo
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'box_update',
                'box_id': data.get('box_id'),
                'box_number': data.get('box_number'),
                'new_status_class': data.get('new_status_class'),
            }
        )

    async def box_update(self, event):
        await self.send(text_data=json.dumps({
            'box_id': event['box_id'],
            'box_number': event['box_number'],
            'new_status_class': event['new_status_class'],
        }))