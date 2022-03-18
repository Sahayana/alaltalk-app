
from dataclasses import dataclass
import json
from datetime import datetime


from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render


from accounts.services.accounts_service import create_user

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
            return redirect("/")  # 채팅템플릿으로 redirect하도록 추후 변경

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
            return redirect("/")  # 채팅템플릿으로 redirect하도록 추후 변경

        return render(request, "accounts/login.html")


@login_required
def logout(request):
    auth.logout(request)
    return redirect("/")


@login_required
def friend_list(request):
    return render(request, "accounts/user_list.html")


@login_required
def mypage(request):
    user = get_user_model().objects.get(id=request.user.id)
    context = {"user" : user}
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