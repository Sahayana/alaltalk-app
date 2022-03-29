import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from accounts.models import CustomUser
from .models import ChatMessage
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        # s = SessionStore()
        # s.create()
        # session_key = s.session_key
        # SessionStore(session_key=session_key)
        # session = Session.objects.get(pk=session_key)
        # print(session)

        messages = ChatMessage.last_10_messages()
        content = {
            "command": "messages",
            "messages": self.messages_to_json(messages)
        }
        self.send_chat_message(content)

    def new_message(self, data):
        user_id = data["from"]
        chatroom_id = data["room_id"]
        author = CustomUser.objects.filter(id=user_id)[0]
        author_id = author.id
        print(author_id)
        message = ChatMessage.objects.create(author_id=author_id, message=data["message"], chatroom_id=chatroom_id)
        content = {"command": "new_message", "message": self.message_to_json(message)}
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            "author": message.author.id,
            "message": message.message,
            "created_at": str(message.created_at),
            "chatroom_id": message.chatroom.id,
        }

    commands = {"fetch_messages": fetch_messages, "new_messages": new_message}

    def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_id = "chat_%s" % self.room_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(self.room_group_id, self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(self.room_group_id, self.channel_name)

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(self.room_group_id, {"type": "chat_message", "message": message})

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))
