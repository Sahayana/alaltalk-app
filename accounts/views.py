import json
import random
from datetime import datetime

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render

from accounts.models import FriendRequest
from accounts.services.accounts_service import (
    accept_friend_request,
    check_authentication,
    check_email_duplication,
    create_single_user,
    decline_friend_request,
    get_friend_list,
    send_friend_request,
)

# Create your views here.


def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        nickname = request.POST.get("nickname")
        password = request.POST.get("password2")
        bio = request.POST.get("bio")
        if request.FILES.get("img"):
            img = request.FILES.get("img")
            create_single_user(email=email, nickname=nickname, password=password, bio=bio, img=img)
        else:
            create_single_user(email=email, nickname=nickname, password=password, bio=bio)
        context = {"result": "회원가입이 완료되었습니다."}
        return JsonResponse(context)

    elif request.method == "GET":
        signed_user = request.user.is_authenticated
        if signed_user:
            return redirect("accounts:mypage")

        return render(request, "accounts/signup.html")


def duplicated_check(request):
    if request.method == "GET":
        email = request.GET.get("email")
        context = {"duplicated": check_email_duplication(email=email)}
        return JsonResponse(context)


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        me = auth.authenticate(email=email, password=password)
        # print(me, email, password)
        if not me:
            return JsonResponse({"msg": "error"})

        auth.login(request, me)
        return JsonResponse({"msg": "ok"})

    else:
        signed_user = request.user.is_authenticated
        if signed_user:
            return redirect("accounts:mypage")

        return render(request, "accounts/login.html")


@login_required
def logout(request):
    auth.logout(request)
    return redirect("/")


@login_required
def friend_list(request):
    user = request.user
    friends = get_friend_list(user_id=user.id)
    context = {
        "user": user,
        "friends": friends,
    }
    return render(request, "accounts/user_list.html", context)


@login_required
def mypage(request):
    user = get_user_model().objects.get(id=request.user.id)
    friend_requests = FriendRequest.objects.filter(receiver=user)
    context = {
        "user": user,
        "friend_requests": friend_requests,
    }
    return render(request, "accounts/mypage.html", context)


@login_required
def profile_change(request):

    user = request.user

    if request.method == "POST":
        nickname = request.POST.get("nickname")
        bio = request.POST.get("bio")
        # print(request.FILES.get("img"))
        if request.FILES.get("img") != None:
            img = request.FILES.get("img")
            img_extension = img.name.split(".")[-1]
            username, domain = user.email.split('@')
            img.name = username + domain.split('.')[0] + domain.split('.')[1] + "-" + datetime.now().strftime("%Y-%m-%d") + "." + img_extension
            user.img = img
        if request.POST.get("password"):
            password = request.POST.get("password")
            user.set_password(password)

        user.nickname = nickname
        user.bio = bio
        user.save()
        return JsonResponse({"msg": "ok"})


@login_required
def search_friend(request):
    user = request.user
    me = get_user_model().objects.filter(id=user.id)

    if request.method == "GET":
        query = request.GET.get("q")
        result = get_user_model().objects.filter(Q(email__icontains=query) | Q(nickname__icontains=query)).distinct()  # 중복 제거를 위한 distinct()

        # 검색으로 나온 유저가 현재 친구인 경우 예외처리 (튜플형태로 숫자 입력)
        result_json = list(result.values())
        for i, friend in enumerate(result_json):
            # print(friend["img"])
            if friend in user.friends.all().values():
                # print("친구입니다")
                result_json[i] = (friend, 0)  # 0 인 경우 이미 친구
            elif friend == me.values()[0]:
                # print("나입니다.")
                result_json[i] = (friend, 1)  # 1 인 경우 자기 자신
            else:
                # print("모르는사이입니다")
                result_json[i] = (friend, 2)  # 2 인 경우 친구가 아닌 상태

        return JsonResponse({"result": result_json})


@login_required
def send_request(request, receiver_id):
    sender = request.user
    receiver = get_user_model().objects.get(id=receiver_id)
    friend_request, created = send_friend_request(sender_id=sender.id, recevier_id=receiver.id)
    if created:
        return JsonResponse({"msg": "sent"})
    return JsonResponse({"msg": "already"})


@login_required
def accept_request(request, request_id):
    user_id = request.user.id
    accept_friend_request(user_id=user_id.id, request_id=request_id)
    return JsonResponse({"msg": "accepted"})


@login_required
def decline_request(request, request_id):
    decline_friend_request(request_id=request_id)
    return JsonResponse({"msg": "declined"})


def temporary_password(request):

    query = request.GET.get("q")
    print(query)
    user = get_user_model().objects.filter(email__iexact=query).get()
    if user is None:
        return JsonResponse({"msg": "none-user"})

    alp_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alp_str_lower = alp_str.lower()
    num = "1234567890"
    temp_pw = "".join(random.sample(alp_str + alp_str_lower + num, k=12))

    user.set_password(temp_pw)
    user.save()

    send_mail("[alaltalk] 임시 비밀번호 메일입니다.", f"회원님의 임시 비밀번호는 {temp_pw} 입니다.\n로그인 후 비밀번호를 꼭 변경해주세요.", "alaltalklove@gmail.com", [user.email], fail_silently=False)

    return JsonResponse({"msg": "ok"})


@login_required
def auth_check(request):
    user_id = request.user.id
    password = request.POST.get("password")

    me = check_authentication(user_id=user_id, password=password)

    if me:
        return JsonResponse({"msg": "ok"})
    else:
        return JsonResponse({"msg": "no"})
