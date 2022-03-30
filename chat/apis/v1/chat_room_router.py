# from typing import Tuple
#
# from ninja import Router
#
# from chat.apis.v1.schemas.chat_room_create_request import ChatRoomCreateRequest
# from chat.apis.v1.schemas.chat_room_response import ChatRoomResponse
# from chat.models import ChatRoom
# from chat.services.chat_service import create_an_chat_room
#
# router = Router()
#
#
# # @router.post("/", response=ChatRoomResponse)
# # def create_chat_room(request: , chatroom_create_request: ChatRoomCreateRequest) -> Tuple[int, ChatRoom]:
# #     chatroom = create_an_chat_room(chatroom_create_request.user1_id, chatroom_create_request.user2_id)
# #     return chatroom
