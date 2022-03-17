from email.policy import EmailPolicy
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
import json
from django.contrib.auth import get_user_model
from accounts.services.accounts_service import create_user
from django.contrib.auth.decorators import login_required
# Create your views here.



def signup(request):
    if request.method == 'POST':        
        email = request.POST.get("email")
        nickname = request.POST.get("nickname")
        password = request.POST.get("password2")
        bio = request.POST.get("bio")
        img = request.FILES.get("img")
        
        create_user(email=email, nickname=nickname, password=password , bio=bio, img=img)
        context = {"result":"회원가입이 완료되었습니다."}
        return JsonResponse(context)
    
    elif request.method == 'GET':
        signed_user = request.user.is_authenticated
        if signed_user:
            return redirect('/')    # 채팅템플릿으로 redirect하도록 추후 변경

        return render(request, 'accounts/signup.html')



def duplicated_check(request):
    if request.method == 'GET':
        email = request.GET.get("email")
        context = {
            "duplicated": get_user_model().objects.filter(email__iexact=email).exists()
        }
        return JsonResponse(context)



def login(request):
    if request.method == 'POST':        
        email = request.POST.get("email")
        password = request.POST.get("password")
        me = auth.authenticate(email=email, password=password)
        print(me, email, password)
        if not me:
            return JsonResponse({"msg":"error"})
        
        auth.login(request, me)
        return JsonResponse({"msg":"ok"})
        
    else:
        signed_user = request.user.is_authenticated
        if signed_user:
            return redirect('/')    # 채팅템플릿으로 redirect하도록 추후 변경

        return render(request, 'accounts/login.html')

        
@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')