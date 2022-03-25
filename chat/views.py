import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt

from accounts.models import CustomUser
from chat.models import ChatMessage, ChatRoom

# # 유저리스트 불러오기
# @login_required
# def get_user_list(request):
#     user_list = CustomUser.objects.all().exclude(is_superuser=True).exclude(id=request.user.id)
#     print(user_list)
#     return render(request, "accounts/user_list.html", {"user_list": user_list})


# userlist 중에 친구신청-수락한 유저 리스트 불러오기
# ChatMessage 모델에서 메세지 불러와서 가장 최근 메세지를 보여줌
@login_required
def show_chat_list(request):
    chat_list = CustomUser.objects.all().exclude(is_superuser=True).exclude(id=request.user.id)
    return render(request, "chat/chat_list.html", {"chat_list": chat_list})


# 채팅하기 버튼 클릭 시 채팅방 생성
# 채팅방에 참여하는 유저가 동일할 경우 새로 생성하지 않고 기존의 채팅을 불러옴
@login_required
def create_chat_room(request, id):
    user = request.user
    print(user.id)
    partner = CustomUser.objects.get(id=id)
    print(partner.id)

    if user == request.user:
        exist_room1 = ChatRoom.objects.filter(participant1=user.id, participant2=partner.id)
        exist_room2 = ChatRoom.objects.filter(participant1=partner.id, participant2=user.id)
        if exist_room1:
            room = ChatRoom.objects.get(participant1=user.id, participant2=partner.id)
            room_id = room.id
            return redirect("/chat/room/" + str(room_id) + "/")
        elif exist_room2:
            room = ChatRoom.objects.get(participant1=partner.id, participant2=user.id)
            room_id = room.id
            return redirect("/chat/room/" + str(room_id) + "/")
        else:
            chat_room = ChatRoom.objects.create(participant1=user.id, participant2=partner.id)
            chat_room.save()

            # ChatRoom에 있는 room id 로 redirect
            room = ChatRoom.objects.get(participant1=user.id, participant2=partner.id)
            room_id = room.id
            return redirect("/chat/room/" + str(room_id) + "/")
    else:
        return render(request, "chat/chat_room.html")


# 웹소켓이 실행되면서 열린 chat/room/room_id html로 데이터 전달
@csrf_exempt
@login_required
def create_chat_message(request, room_id):
    # user = request.user
    # chatroom = ChatRoom.objects.get(id=room_id)
    # print(chatroom.participant1, chatroom.participant2, user.id)
    # if chatroom.participant1 == user.id or chatroom.participant2 == user.id:
    #     chat_list = CustomUser.objects.all().exclude(is_superuser=True).exclude(id=request.user.id)
    #     # last_message = ChatMessage.objects.filter(chatroom_id=room_id).latest('chatroom_id')
    #     # print(last_message.message)
    #     return render(
    #         request,
    #         "chat/chat_room.html",
    #         {
    #             "room_id": mark_safe(json.dumps(room_id)),
    #             "chat_list": chat_list,
    #             "user_id": mark_safe(json.dumps(request.user.id)),
    #             # 'last_message': last_message.message,
    #         },
    #     )
    # else:
    #     return redirect('/chat')

    if request.method == "GET":
        user = request.user
        chatroom = ChatRoom.objects.get(id=room_id)
        print(chatroom.participant1, chatroom.participant2, user.id)
        chat_list = CustomUser.objects.all().exclude(is_superuser=True).exclude(id=request.user.id)
        # last_message = ChatMessage.objects.filter(chatroom_id=room_id).latest('chatroom_id')
        # print(last_message.message)
        return render(
            request,
            "chat/chat_room.html",
            {
                "room_id": mark_safe(json.dumps(room_id)),
                "chat_list": chat_list,
                "user_id": mark_safe(json.dumps(request.user.id)),
                "participant1": chatroom.participant1,
                "participant2": chatroom.participant2,
                # 'last_message': last_message.message,
            },
        )
