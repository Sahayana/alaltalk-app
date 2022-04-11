import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from accounts.models import CustomUser
from .models import ChatMessage


class ChatConsumer(WebsocketConsumer):
    # 이전 메세지 불러오기
    def fetch_messages(self, data):
        messages = ChatMessage.last_10_messages()
        content = {
            "command": "messages",
            "messages": self.messages_to_json(messages)
        }
        self.send_chat_message(content)

    # 새로운 메세지 DB에 저장하기
    def new_message(self, data):
        user_id = data["from"]
        chatroom_id = data["room_id"]
        author = CustomUser.objects.filter(id=user_id)[0]
        author_id = author.id
        print("컨슈머가 DB 저장", author_id)
        message = ChatMessage.objects.create(author_id=author_id, message=data["message"], chatroom_id=chatroom_id)
        content = {"command": "new_message", "message": self.message_to_json(message)}
        return self.send_chat_message(content)

    # DB에서 불러온 이전 메세지를 리스트 형태로 변환
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    # 리스트 형태로 변환된 메세지를 key:value 형태로 반환
    def message_to_json(self, message):
        return {
            "author": message.author.id,
            "message": message.message,
            "created_at": str(message.created_at),
            "chatroom_id": message.chatroom.id,
        }

    # commands에 따라 실행되는 함수를 제어
    commands = {"fetch_messages": fetch_messages, "new_messages": new_message}

    # 웹소켓에 연결 되었을 때의 동작
    def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_id = "chat_%s" % self.room_id

        # room_id를 통해 그룹에 들어가기
        async_to_sync(self.channel_layer.group_add)(self.room_group_id, self.channel_name)

        self.accept()

    # 웹소켓 연결이 끊어 졌을 때의 동작
    def disconnect(self, close_code):
        # 그룹에서 나오기
        async_to_sync(self.channel_layer.group_discard)(self.room_group_id, self.channel_name)
        print('websocket closed')

    # commands 를 통해 데이터 받아오기
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)

    # room_id로 묶인 그룹에 메세지 보내주기
    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(self.room_group_id, {"type": "chat_message", "message": message})

    # 메세지는 json이나 바이너리 형태로 전송
    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # room_id로 묶인 그룹에서 메세지 받기
    # 웹소켓으로 메세지 전달
    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))
