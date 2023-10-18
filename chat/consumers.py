import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import ChatModel, Userprofilemodel
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        current_user_id = self.scope['user'].id
        # getting the current user id
        other_user_id = self.scope['url_route']['kwargs']['id']
        # getting the user id with whom current he will be chatting as it is a personal chat app
        # so only two persons will be in a chat room
        
        if int(current_user_id) > int(other_user_id):
            self.room_name = f'{current_user_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{current_user_id}'
            
        self.room_group_name = 'chat_%s' % self.room_name
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        # await self.send(text_data=self.room_group_name)
        
    async def disconnect(self, code):
         self.channel_layer.group_discard(self.room_group_name, self.channel_layer)
        
    
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        
        await self.save_message(username,self.room_group_name,message)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message' : message,
                'username': username
            }
        )
        
    async def chat_message(self,event):
        message = event['message']
        username = event['username']
        
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
    
    # We need to use this decorator when we need to deal with databases or models in django channels
    @database_sync_to_async
    def save_message(self, username, thread_name ,message):
        ChatModel.objects.create(sender=username,message=message,thread_name=thread_name)
        
class OnlineStatusConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_group_name = 'user'
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        
    
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        username = data['username']
        connection_type = data['type']
        print(connection_type)
        await self.change_status(username,connection_type)
        
    async def send_onlineStatus(self, event):
        data = json.loads(event.get('value'))
        username = data['username']
        online_status = data['status']
        
        await self.send(text_data=json.dumps({
            'username': username,
            'online_status': online_status
        }))
        
    async def disconnect(self, message):
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        
    @database_sync_to_async
    def change_status(self, username, connection_type):
        user = User.objects.get(username=username)
        userProfile = Userprofilemodel.objects.get(user=user)
        
        if connection_type == 'open':
            userProfile.online_status = True
            userProfile.save()
        else:
            userProfile.online_status = False
            userProfile.save()