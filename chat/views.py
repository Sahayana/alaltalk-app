import json

from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from accounts.models import CustomUser
from chat.models import ChatMessage, ChatRoom
from search.models import Youtube,News,Book,Shopping


# ChatRoom 모델에서 유저가 속해있는 채팅방 리스트 불러오기
# ChatMessage 모델에서 마지막 메세지 출력
@login_required
def show_chat_list(request):
    user = request.user
    chatroom_list = ChatRoom.objects.filter(Q(participant1=user) | Q(participant2=user)).all()
    all_message = ChatMessage.objects.all()
    return render(request, "chat/chat_list.html", {"chatroom_list": chatroom_list, "all_message": all_message})


# 채팅하기 버튼 클릭 시 채팅방 생성
# 채팅방에 참여하는 유저가 동일할 경우 새로 생성하지 않고 기존의 채팅을 불러옴
@login_required
def create_chat_room(request, id):
    user = request.user
    print(user)
    partner = CustomUser.objects.get(id=id)
    print(partner)

    if user == request.user:
        exist_room1 = ChatRoom.objects.filter(participant1=user, participant2=partner)
        exist_room2 = ChatRoom.objects.filter(participant1=partner, participant2=user)
        if exist_room1:
            room = ChatRoom.objects.get(participant1=user, participant2=partner)
            room_id = room.id
            return redirect("/chat/room/" + str(room_id) + "/")
        elif exist_room2:
            room = ChatRoom.objects.get(participant1=partner, participant2=user)
            room_id = room.id
            return redirect("/chat/room/" + str(room_id) + "/")
        else:
            chat_room = ChatRoom.objects.create(participant1=user, participant2=partner)
            chat_room.save()

            # ChatRoom에 있는 room id 로 redirect
            room = ChatRoom.objects.get(participant1=user, participant2=partner)
            room_id = room.id
            return redirect("/chat/room/" + str(room_id) + "/")
    else:
        return render(request, "chat/chat_room.html")


# 웹소켓이 실행되면서 열린 chat/room/room_id html로 데이터 전달
@csrf_exempt
@login_required
def post_data_to_chat_room(request, room_id):
    if request.method == "GET":
        user = request.user
        chatroom = ChatRoom.objects.get(id=room_id)
        chatroom_list = ChatRoom.objects.filter(Q(participant1=user) | Q(participant2=user)).all()
        all_message = ChatMessage.objects.all()

        last_messages = ChatMessage.objects.filter(chatroom_id=room_id).order_by("created_at")
        limit = len(last_messages) - 20
        if len(last_messages) > 20:
            last_messages = last_messages[limit:]
        # latest_created_message = ChatMessage.objects.filter(chatroom_id=room_id).order_by('-created_at')[0]

        if chatroom.participant1.id == user.id:
            participant = chatroom.participant2
            participant_like_youtube = Youtube.objects.filter(user=chatroom.participant2)
            participant_like_news = News.objects.filter(user=chatroom.participant2)
            participant_like_book = Book.objects.filter(user=chatroom.participant2)
            participant_like_shopping = Shopping.objects.filter(user=chatroom.participant2)
        else :
            participant = chatroom.participant1
            participant_like_youtube = Youtube.objects.filter(user=chatroom.participant1)
            participant_like_news = News.objects.filter(user=chatroom.participant1)
            participant_like_book = Book.objects.filter(user=chatroom.participant1)
            participant_like_shopping = Shopping.objects.filter(user=chatroom.participant1)

        return render(
            request,
            "chat/chat_room.html",
            {
                "room_id": mark_safe(json.dumps(room_id)),
                "chatroom_list": chatroom_list,
                "user_id": mark_safe(json.dumps(request.user.id)),
                "participant1": chatroom.participant1,
                "participant2": chatroom.participant2,
                "participant": participant,
                "all_message": all_message,
                "last_messages": last_messages,
                # "latest_created_message": latest_created_message,
                "participant_like_youtube": participant_like_youtube,
                "participant_like_news": participant_like_news,
                "participant_like_book": participant_like_book,
                "participant_like_shopping": participant_like_shopping,
            },
        )


@csrf_exempt
@login_required
def chat_log_send(request):
    room_id = json.loads(request.body.decode('utf-8'))['room_id']
    chat_log = []
    print(room_id)
    chatroom = ChatRoom.objects.get(id = room_id)
    all_chat = ChatMessage.objects.filter(chatroom=chatroom)
    print(len(all_chat))
    if len(all_chat) > 40:
        all_chat = all_chat[len(all_chat)-40:]

    for chat in all_chat:
        chat_log.append(chat.message)
    print('채팅로그 담긴리스트',chat_log)
    context = {
        'chat_log' : chat_log
    }
    return HttpResponse(json.dumps(context), content_type="application/json")
