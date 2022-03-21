
from dataclasses import dataclass
import json
from datetime import datetime
import random

from django.db.models import Q
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.core.mail import send_mail

from accounts.services.accounts_service import create_user
from accounts.models import FriendRequest

# Create your views here.


def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        nickname = request.POST.get("nickname")
        password = request.POST.get("password2")
        bio = request.POST.get("bio")
        img = request.FILES.get("img")

        create_user(email=email, nickname=nickname, password=password, bio=bio, img=img)
        context = {"result": "회원가입이 완료되었습니다."}
        return JsonResponse(context)

    elif request.method == "GET":
        signed_user = request.user.is_authenticated
        if signed_user:
            return redirect("accounts:mypage")  # 채팅템플릿으로 redirect하도록 추후 변경

        return render(request, "accounts/signup.html")


def duplicated_check(request):
    if request.method == "GET":
        email = request.GET.get("email")
        context = {"duplicated": get_user_model().objects.filter(email__iexact=email).exists()}
        return JsonResponse(context)


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        me = auth.authenticate(email=email, password=password)
        print(me, email, password)
        if not me:
            return JsonResponse({"msg": "error"})

        auth.login(request, me)
        return JsonResponse({"msg": "ok"})

    else:
        signed_user = request.user.is_authenticated
        if signed_user:
            return redirect("accounts:mypage")  # 채팅템플릿으로 redirect하도록 추후 변경

        return render(request, "accounts/login.html")


@login_required
def logout(request):
    auth.logout(request)
    return redirect("/")


@login_required
def friend_list(request):
    user = get_user_model().objects.get(id=request.user.id)
    friends = user.friends.all()
    print(friends)
    context = {
        'user':user,
        'friends': friends,
        }
    return render(request, "accounts/user_list.html", context)


@login_required
def mypage(request):
    user = get_user_model().objects.get(id=request.user.id)
    friend_requests = FriendRequest.objects.filter(receiver=user)
    context = {
        "user" : user,
        "friend_requests": friend_requests,
    }
    return render(request, "accounts/mypage.html", context)

@login_required
def profile_change(request):

    user = request.user

    if request.method == 'POST':
        nickname = request.POST.get("nickname")
        bio = request.POST.get("bio")        
        if request.FILES.get("img") != None:
            img = request.FILES.get("img")
            img_extension = img.name.split('.')[-1]
            img.name = user.email.split('@')[0]+ '-' + datetime.now().strftime('%Y-%m-%d') + '.' + img_extension
            user.img = str(img)

        user.nickname = nickname
        user.bio = bio        
        user.save()
        return JsonResponse({"msg":"ok"})


@login_required
def search_friend(request):
    user = request.user # 자기 자신을 검색한 경우 예외처리 남음
    
    if request.method == 'GET':
        query = request.GET.get("q")
        result = get_user_model().objects.filter(
            Q(email__icontains=query) |
            Q(nickname__icontains=query)
        ).distinct()    # 중복 제거를 위한 distinct()
        result = result.values() # serialized        

        return JsonResponse({"result":list(result)})



@login_required
def send_request(request, receiver_id):
    sender = request.user
    receiver = get_user_model().objects.get(id=receiver_id)
    friend_request, created = FriendRequest.objects.get_or_create(sender=sender, receiver=receiver)
    if created:
        return JsonResponse({"msg":"sent"})
    return JsonResponse({"msg":"already"})


@login_required
def accept_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.receiver == request.user:
        friend_request.receiver.friends.add(friend_request.sender)
        friend_request.sender.friends.add(friend_request.receiver)
        friend_request.delete()
        return JsonResponse({"msg":"accepted"})
    else:
        return JsonResponse({"msg":"error"})    # 거절, 회수 등의 예외처리 남음


def temporary_password(request):
    
    query = request.GET.get("q")
    print(query)
    user = get_user_model().objects.filter(email__iexact=query).get()
    if user is None:
        return JsonResponse({"msg":"none-user"})
    
    alp_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alp_str_lower = alp_str.lower()
    num = '1234567890'
    temp_pw = ''.join(random.sample(alp_str+alp_str_lower+num, k=12))

    user.set_password(temp_pw)
    user.save()
    
    send_mail(
        "[alaltalk] 임시 비밀번호 메일입니다.",
        f"회원님의 임시 비밀번호는 {temp_pw} 입니다.\n로그인 후 비밀번호를 꼭 변경해주세요.",
        'alaltalklove@gmail.com',
        [user.email],
        fail_silently=False
    )

    return JsonResponse({"msg":"ok"})
    
    
    
    

    