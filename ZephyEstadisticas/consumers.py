import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .dashboard import obtener_estadisticas
import asyncio
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

class EstadoBoxDashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        await self.channel_layer.group_add("dashboard", self.channel_name)
        await self.accept()


        data = await obtener_estadisticas()
        await self.send(text_data=json.dumps(data))


        self.update_task = asyncio.create_task(self.send_periodically())

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard("dashboard", self.channel_name)
        
        self.update_task.cancel()

    async def dashboard_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    async def send_periodically(self):
        while True:
            await asyncio.sleep(1) 
            data = await obtener_estadisticas()  
            await self.send(text_data=json.dumps(data)) 