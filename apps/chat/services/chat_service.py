from chat.models import ChatRoom


def create_an_chat_room(user1_id: int, user2_id: int) -> ChatRoom:
    return ChatRoom.objects.create(user1_id=user1_id, user2_id=user2_id)


def get_an_chat_room(room_id: int, user_id: int) -> ChatRoom:
    return ChatRoom.objects.filter(user_id=user_id).get(id=room_id)


def delete_an_chat_room(room_id: int) -> None:
    ChatRoom.objects.filter(id=room_id).delete()
