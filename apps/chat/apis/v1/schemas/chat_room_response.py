from ninja import Schema


class ChatRoomResponse(Schema):
    room_id: int
    user1_id: int
    user2_id: int
