import json

from accounts.models import CustomUser
from accounts.utils import LoginConfirm
from chat.models import ChatMessage, ChatRoom
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from search.models import Book, News, Shopping, Youtube


# ChatRoom 모델에서 유저가 속해있는 채팅방 리스트 불러오기
@LoginConfirm
def show_chat_list(request):
    user = request.user
    chatroom_list = (
        ChatRoom.objects.filter(Q(participant1=user) | Q(participant2=user))
        .all()
        .order_by("-created_at")
    )
    all_message = ChatMessage.objects.all()
    return render(
        request,
        "chat/chat_list.html",
        {
            "user_id": user.id,
            "chatroom_list": chatroom_list,
            "all_message": all_message,
        },
    )


# 채팅하기 버튼 클릭 시 채팅방 생성
# 채팅방에 참여하는 유저가 동일할 경우 새로 생성하지 않고 기존의 채팅을 불러옴
@LoginConfirm
def create_chat_room(request, id):
    user = request.user
    partner = CustomUser.objects.get(id=id)

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
            try:
                chat_room = ChatRoom.objects.create(
                    participant1=user, participant2=partner
                )
                chat_room.save()

                # ChatRoom에 있는 room id 로 redirect
                room = ChatRoom.objects.get(participant1=user, participant2=partner)
                room_id = room.id
                return redirect("/chat/room/" + str(room_id) + "/")
            except exist_room1.DoesNotExist or exist_room1.DoesNotExist:
                return render(
                    request, "chat/chat_room.html", {"error": "존재하지 않거나 사라진 채팅방입니다."}
                )

    else:
        return render(request, "chat/chat_room.html", {"error": "접근 불가한 채팅방 입니다."})


# room_id로 채팅방 삭제
@csrf_exempt
@LoginConfirm
def delete_chat_room(request, room_id):
    target_room = ChatRoom.objects.get(id=room_id)
    target_room.delete()
    return redirect("/chat")


# 웹소켓이 실행되면서 열린 html로 데이터 전달
@csrf_exempt
@LoginConfirm
def post_data_to_chat_room(request, room_id):
    if request.method == "GET":
        user = request.user
        chatroom = ChatRoom.objects.get(id=room_id)
        chatroom_list = (
            ChatRoom.objects.filter(Q(participant1=user) | Q(participant2=user))
            .all()
            .order_by("-created_at")
        )
        all_message = ChatMessage.objects.all()

        if chatroom.participant1.id == user.id:
            participant = chatroom.participant2
            participant_like_youtube = Youtube.objects.filter(
                user=chatroom.participant2
            )
            participant_like_news = News.objects.filter(user=chatroom.participant2)
            participant_like_book = Book.objects.filter(user=chatroom.participant2)
            participant_like_shopping = Shopping.objects.filter(
                user=chatroom.participant2
            )
        else:
            participant = chatroom.participant1
            participant_like_youtube = Youtube.objects.filter(
                user=chatroom.participant1
            )
            participant_like_news = News.objects.filter(user=chatroom.participant1)
            participant_like_book = Book.objects.filter(user=chatroom.participant1)
            participant_like_shopping = Shopping.objects.filter(
                user=chatroom.participant1
            )

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
                "participant_like_youtube": participant_like_youtube,
                "participant_like_news": participant_like_news,
                "participant_like_book": participant_like_book,
                "participant_like_shopping": participant_like_shopping,
            },
        )


# AI API로 전달할 채팅로그
@csrf_exempt
@LoginConfirm
def chat_log_send(request):
    room_id = json.loads(request.body.decode("utf-8"))["room_id"]
    chat_log = []
    sentence = ""
    chatroom = ChatRoom.objects.get(id=room_id)
    all_chat = ChatMessage.objects.filter(chatroom=chatroom)

    if len(all_chat) > 40:
        all_chat = all_chat[len(all_chat) - 40 :]

    for chat in all_chat:
        sentence = sentence + chat.message + " "

    chat_log.append(sentence)

    context = {"chat_log": chat_log}
    return HttpResponse(json.dumps(context), content_type="application/json")


# 채팅방의 이전메세지 더보기(버튼 클릭시 10개씩 로드)
@csrf_exempt
@LoginConfirm
def more_list(request):
    room_id = json.loads(request.body.decode("utf-8"))["room_id"]
    num = json.loads(request.body.decode("utf-8"))["startNum"]
    # user_id = json.loads(request.body.decode("utf-8"))["user_id"]

    all_chat = ChatMessage.objects.filter(chatroom_id=room_id).order_by("created_at")
    if all_chat is not None:
        all_chat = all_chat[num : num + 10]
        if all_chat is None:
            all_chat = all_chat[num:]

    chat_list = []
    for chat in all_chat:
        chat_list.append(
            {
                "message": chat.message,
                "author_id": chat.author_id,
                "created_at": str(chat.created_at),
            }
        )

    context = {"chat_list": chat_list}

    return HttpResponse(json.dumps(context), content_type="application/json")


# 채팅방 이전메세지 로더
@csrf_exempt
@LoginConfirm
def message_loader(request):
    room_id = json.loads(request.body.decode("utf-8"))["room_id"]
    last_messages = ChatMessage.objects.filter(chatroom_id=room_id).order_by(
        "created_at"
    )
    limit = len(last_messages) - 40
    if len(last_messages) > 40:
        last_messages = last_messages[limit:]

    last_messages_list = []
    for chat in last_messages:
        last_messages_list.append(
            {
                "message": chat.message,
                "author_id": chat.author_id,
                "created_at": str(chat.created_at),
            }
        )

    context = {"last_messages_list": last_messages_list}

    return HttpResponse(json.dumps(context), content_type="application/json")


# 채팅방 별 최신 메세지 1개 뽑기
@csrf_exempt
@LoginConfirm
def latest_message_not_connected(request):
    partner_list = json.loads(request.body.decode("utf-8"))["partner_list"]

    latest_chat_list = []
    for partner in partner_list:

        chatter = CustomUser.objects.get(id=partner)
        chatroom = ChatRoom.objects.get(
            Q(participant1=request.user, participant2_id=chatter)
            | Q(participant2=request.user, participant1=chatter)
        )

        latest_message_each_chatroom = ChatMessage.objects.filter(
            chatroom=chatroom
        ).order_by("-created_at")
        for message in latest_message_each_chatroom:
            if message is latest_message_each_chatroom[0]:

                latest_chat_list.append(
                    {
                        "partner": chatter.id,
                        "author_message": message.author_id,
                        "latest_message_each_chatroom": message.message,
                    }
                )

    context = {
        "latest_chat_list": latest_chat_list,
    }

    return HttpResponse(json.dumps(context), content_type="application/json")


# partner_id로 chatroom을 찾아 list 형태로 전달
@csrf_exempt
@LoginConfirm
def get_room_id(request):
    partner_list = json.loads(request.body.decode("utf-8"))["partner_list"]

    room_list = []
    for partner in partner_list:
        chatter = CustomUser.objects.get(id=partner)
        chatroom = ChatRoom.objects.filter(
            Q(participant1=request.user, participant2_id=chatter)
            | Q(participant2=request.user, participant1=chatter)
        )

        for room in chatroom:
            room_list.append(room.id)

    context = {
        "room_list": room_list,
    }

    return HttpResponse(json.dumps(context), content_type="application/json")
