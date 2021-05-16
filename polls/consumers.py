import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from time import sleep
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import random
   
class CrawPredictConsume(AsyncWebsocketConsumer):
    # Connected to websocket.connect
    async def connect(self):
        #self.scope["session"]["seed"] = random.randint(1, 10000)

        await self.accept()

    async def disconnect(self,close_code):

        print("disc")

    async def receive(self, text_data):
        datapoint = json.loads(text_data)
        val =datapoint['message']
        print(val)
        for i in range(0,100):
            await asyncio.sleep(2)
            await self.send(text_data=json.dumps(str(i)))


