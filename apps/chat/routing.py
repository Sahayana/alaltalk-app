# 유저를 대신하여 consumers와 연결해주는 router 생성
from django.urls import re_path

from apps.chat import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/room/(?P<room_id>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
