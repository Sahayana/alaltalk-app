from datetime import datetime
from typing import Tuple

from django.contrib import auth
from django.db.models import QuerySet
from django.dispatch import receiver

from accounts.models import CustomUser, FriendRequest


def create_single_user(email: str, nickname: str, password: str, **kwargs: str) -> CustomUser:
    user = CustomUser.objects.create_user(email=email, nickname=nickname, password=password, **kwargs)
    return user


def check_email_duplication(email: str) -> bool:
    return CustomUser.objects.filter(email__iexact=email).exists()


# def change_user_profile(user: CustomUser, nickname:str, bio:str, **kwargs: str) -> CustomUser:
#     user.nickname = nickname
#     user.bio = bio
#     # img = kwargs.get('img','')
#     try:
#         img = kwargs['img']
#         img_extension = img.name.split(".")[-1]
#         img.name = user.email.split("@")[0] + "-" + datetime.now().strftime("%Y-%m-%d") + "." + img_extension
#         user.img = img
#     except:
#         pass

#     try:
#         password = kwargs['password']
#         user.set_password(password)
#     except:
#         pass
#     user.save()
#     return user


def get_friend_list(user_id: int) -> QuerySet[CustomUser]:
    user = CustomUser.objects.get(id=user_id)
    friends = user.friends.all()
    return friends


# def get_mypage(user_id: int) -> Tuple(CustomUser, QuerySet[CustomUser]):
#     user = CustomUser.objects.get(id=user_id)
#     friend_requests = FriendRequest.objects.filter(receiver=user)
#     return user, friend_requests


def send_friend_request(sender_id: int, recevier_id: int) -> Tuple[CustomUser, bool]:
    friend_request, is_created = FriendRequest.objects.get_or_create(sender_id=sender_id, receiver_id=recevier_id)
    return friend_request, is_created


def accept_friend_request(user_id: int, request_id: int) -> None:
    user = CustomUser.objects.get(id=user_id)
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.receiver == user:
        friend_request.receiver.friends.add(friend_request.sender)
        friend_request.sender.friends.add(friend_request.receiver)
        friend_request.delete()


def decline_friend_request(request_id: int) -> None:
    FriendRequest.objects.filter(id=request_id).delete()


def check_authentication(user_id: int, password: str) -> CustomUser:
    user = CustomUser.objects.get(id=user_id)
    me = auth.authenticate(email=user.email, password=password)
    return me
