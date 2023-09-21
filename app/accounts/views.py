import json
import random
from datetime import datetime

from accounts.apps import W2V
from accounts.models import CustomUser, FriendRequest
from accounts.services.accounts_service import (
    accept_friend_request,
    accounts_delete_friend,
    accounts_profile_delete,
    accounts_search_friends,
    accounts_token_authenticated,
    check_authentication,
    check_email_duplication,
    create_single_user,
    decline_friend_request,
    get_friend_list,
    send_email_verification,
    send_friend_request,
    verified_email_activation,
)
from accounts.utils import LoginConfirm
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.core.mail import send_mail
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from search.models import Book, News, Shopping, Youtube

# Create your views here.


def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        nickname = request.POST.get("nickname")
        password = request.POST.get("password2")
        bio = request.POST.get("bio")
        if request.FILES.get("img"):
            img = request.FILES.get("img")
            user = create_single_user(
                email=email, nickname=nickname, password=password, bio=bio, img=img
            )
        else:
            user = create_single_user(
                email=email, nickname=nickname, password=password, bio=bio
            )

        current_site = get_current_site(request)
        current_site_domain = current_site.domain
        result = send_email_verification(user=user, current_domain=current_site_domain)
        if result == 1:
            return JsonResponse({"msg": "sent"}, status=200)
        else:
            return JsonResponse({"msg": "error"}, status=200)

    elif request.method == "GET":
        signed_user = request.user.is_authenticated
        if signed_user and signed_user.is_active:
            return redirect("accounts:mypage")

        return render(request, "accounts/signup.html")


def duplicated_check(request):
    if request.method == "GET":
        email = request.GET.get("email")
        context = {"duplicated": check_email_duplication(email=email)}
        return JsonResponse(context, status=200)


def account_activation(request, uidb64, token):
    verified_email_activation(uidb64=uidb64, token=token)
    return redirect("accounts:login")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        token = accounts_token_authenticated(user_email=email, user_password=password)
        return JsonResponse({"token": token})

    elif request.method == "GET":
        try:
            token = request.COOKIES["Authorization"]
            return redirect("accounts:mypage")
        except KeyError:
            return render(request, "accounts/login.html")


# def login(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         me = auth.authenticate(email=email, password=password)
#         # print(me, email, password)
#         if me and me.is_active:
#             auth.login(request, me)
#             return JsonResponse({"msg": "ok"})
#         else:
#             return JsonResponse({"msg": "error"})

#     else:
#         signed_user = request.user.is_authenticated
#         if signed_user:
#             return redirect("accounts:mypage")

#         return render(request, "accounts/login.html")


@LoginConfirm
def logout(request):
    response = redirect("/")
    response.delete_cookie("Authorization")
    return response


@LoginConfirm
def friend_list(request):
    user = request.user
    friends = get_friend_list(user_id=user.id)
    total_recommend_friend = recommend_friend(user)
    context = {
        "user": user,
        "friends": friends,
        "recommend_friend": total_recommend_friend,
    }
    return render(request, "accounts/user_list.html", context)


@LoginConfirm
def mypage(request):
    user = get_user_model().objects.get(id=request.user.id)
    friend_requests = FriendRequest.objects.filter(receiver=user)
    context = {
        "user": user,
        "friend_requests": friend_requests,
        "youtubes": user.youtube.all(),
        "news": user.news.all(),
        "books": user.book.all(),
        "shoppings": user.shopping.all(),
    }
    return render(request, "accounts/mypage.html", context)


@LoginConfirm
def profile_change(request):

    user = request.user

    if request.method == "POST":
        nickname = request.POST.get("nickname")
        bio = request.POST.get("bio")
        # print(request.FILES.get("img"))
        if request.FILES.get("img") is not None:
            img = request.FILES.get("img")
            img_extension = img.name.split(".")[-1]
            username, domain = user.email.split("@")
            img.name = (
                username
                + domain.split(".")[0]
                + domain.split(".")[1]
                + "-"
                + datetime.now().strftime("%Y-%m-%d")
                + "."
                + img_extension
            )
            user.img = img
        if request.POST.get("password"):
            password = request.POST.get("password")
            user.set_password(password)

        user.nickname = nickname
        user.bio = bio
        user.save()
        return JsonResponse({"msg": "ok"})


@LoginConfirm
def search_friend(request, *args, **kwargs):
    user_id = request.user.id
    context = []
    if request.method == "GET":
        query = request.GET.get("q")
        search_users = accounts_search_friends(user_id=user_id, query=query)
        for user, i in search_users:
            data = {
                "id": user.id,
                "email": user.email,
                "nickname": user.nickname,
                "img": user.img.url,
                "is_friend": i,
            }
            context.append(data)
    return JsonResponse({"result": context}, safe=False)


@LoginConfirm
def send_request(request, receiver_id):
    sender = request.user
    receiver = get_user_model().objects.get(id=receiver_id)
    friend_request, created = send_friend_request(
        sender_id=sender.id, recevier_id=receiver.id
    )
    if created:
        return JsonResponse({"msg": "sent"}, status=201)
    return JsonResponse({"msg": "already"})


@LoginConfirm
def accept_request(request, request_id):
    user_id = request.user.id
    accept_friend_request(user_id=user_id, request_id=request_id)
    return JsonResponse({"msg": "accepted"})


@LoginConfirm
def decline_request(request, request_id):
    decline_friend_request(request_id=request_id)
    return JsonResponse({"msg": "declined"})


def temporary_password(request):

    query = request.GET.get("q")
    try:
        user = get_user_model().objects.get(email=query)
    except CustomUser.DoesNotExist:
        return JsonResponse({"msg": "none-user"})

    alp_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alp_str_lower = alp_str.lower()
    num = "1234567890"
    temp_pw = "".join(random.sample(alp_str + alp_str_lower + num, k=12))

    user.set_password(temp_pw)
    user.save()

    send_mail(
        "[alaltalk] 임시 비밀번호 메일입니다.",
        f"회원님의 임시 비밀번호는 {temp_pw} 입니다.\n로그인 후 비밀번호를 꼭 변경해주세요.",
        "alaltalklove@gmail.com",
        [user.email],
        fail_silently=False,
    )

    return JsonResponse({"msg": "ok"})


@LoginConfirm
def auth_check(request):
    user_id = request.user.id
    password = request.POST.get("password")

    authenticated = check_authentication(user_id=user_id, password=password)

    if authenticated:
        return JsonResponse({"msg": "ok"})
    else:
        return JsonResponse({"msg": "no"})


@LoginConfirm
def profile_delete(request):
    user_id = request.user.id
    accounts_profile_delete(user_id=user_id)
    return JsonResponse({"msg": "deleted"})


@LoginConfirm
def remove_friend(request, friend_id):
    user_id = request.user.id
    accounts_delete_friend(user_id=user_id, friend_id=friend_id)
    return JsonResponse({"msg": "deleted"})


##################### 추천친구 관련 #####################################
@csrf_exempt
@LoginConfirm
def get_user(request):
    user = request.user
    like_sentence = []
    sentence = ""
    youtube = Youtube.objects.filter(user_id=user.id)
    news = News.objects.filter(user_id=user.id)
    book = Book.objects.filter(user_id=user.id)
    shopping = Shopping.objects.filter(user_id=user.id)

    if youtube:
        for y in youtube:
            sentence = sentence + y.title + " "
    if news:
        for n in news:
            sentence = sentence + n.title + " "

    if book:
        for b in book:
            sentence = sentence + b.title + " "

    if shopping:
        for s in shopping:
            sentence = sentence + s.title + " "

    like_sentence.append(sentence)
    print("찜 기반 제목들", sentence)
    context = {"like_sentence": like_sentence}
    return HttpResponse(json.dumps(context), content_type="application/json")


# 키워드 받아서 저장
@LoginConfirm
def save_like_keyword(request):
    user = request.user
    like_keyowrd = json.loads(request.body.decode("utf-8"))["like_keyowrd"]
    user.like_keyword = like_keyowrd
    user.save()
    return JsonResponse({"msg": "add like"})


def recommend_friend(me):
    user = me
    all_user = CustomUser.objects.all().exclude(id=user.id)
    friends = user.friends.all()
    not_friends = []
    recommend_friends = []
    for x in all_user:
        if x not in friends:
            not_friends.append(x)

    simil_user = {}
    user_keyword = user.like_keyword
    if len(not_friends) < 6:
        recommend_friends = not_friends
    else:
        if user_keyword == "":
            recommend_friends = random.sample(not_friends, 5)
        else:
            for friendx in not_friends:
                try:
                    similarity = W2V.model.wv.similarity(
                        user_keyword, friendx.like_keyword
                    )
                    simil_user[friendx.id] = int(similarity * 100)
                except Exception:
                    simil_user[friendx.id] = 0

            print("키워드 유사도", simil_user)
            sorted_friend = sorted(simil_user.items(), key=lambda x: -x[1])
            if len(sorted_friend) > 4:
                for i in sorted_friend[:5]:
                    recommend = CustomUser.objects.get(id=i[0])
                    recommend_friends.append(recommend)
            else:
                for i in sorted_friend:
                    recommend = CustomUser.objects.get(id=i[0])
                    recommend_friends.append(recommend)

    print("추천친구 목록", recommend_friends)
    return recommend_friends


# 친구 관심키워드
@LoginConfirm
def friend_like_recommend(request):
    friend_id = request.GET.get("friend_id")
    friend = CustomUser.objects.get(id=friend_id)
    friend_keyword = friend.like_keyword
    friend_like_keywords = []
    if friend_keyword == "":
        friend_like_keywords.append("찜 없음")

    else:
        friend_like_keywords.append(friend_keyword)
        try:
            similar_word = W2V.model.wv.most_similar(friend_keyword)
            for word in similar_word[:3]:
                friend_like_keywords.append(word[0])
        except Exception:
            pass

    context = {"friend_keywords": friend_like_keywords}
    return HttpResponse(json.dumps(context), content_type="application/json")


##################################################################################################################


@LoginConfirm
def like_public_setting(request):
    value = request.POST["value"]
    print(value)
    if value == "ON":
        change_value = True
    elif value == "OFF":
        change_value = False
    else:
        return JsonResponse({"result": "value is Wrong"})

    user = CustomUser.objects.get(pk=request.user.id)
    user.is_like_public = change_value
    user.save()

    result = "success"
    data = {"result": result}
    return JsonResponse(data)
