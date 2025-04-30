import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.roomGroupName = "group_chat_gfg"
        await self.channel_layer.group_add(
            self.roomGroupName ,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self , close_code):
        self.roomGroupName = "group_chat_gfg"
        # print(close_code)
        await self.channel_layer.group_discard(
            self.roomGroupName , 
            self.channel_name 
        )

    async def chat_message(self , event):
        message = event['message']
        message_type = event.get('message_type', 'text')

        await self.send(text_data=json.dumps({
            'message': message,
            'message_type': message_type,
        }))

    async def receive(self, text_data):

        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        # username = text_data_json["username"]
        data = json.loads(text_data)
        message_type = data.get('type', 'text')
        username = data.get('username', 'Unknown')

        if message_type == 'video':
            await self.channel_layer.group_send(
                self.roomGroupName,
                {
                    'type': 'chat_message',
                    'message': message,
                    'message_type': 'video',
                    'username': username,
                }
            )
        else:
            await self.channel_layer.group_send(
                self.roomGroupName,{
                    "type" : "sendMessage" ,
                    "message" : message , 
                    "username" : username ,
                })
        
        
    async def sendMessage(self , event) : 
        message = event["message"]
        username = event["username"]
        await self.send(text_data = json.dumps({"message":message ,"username":username}))