from datetime import datetime
from typing import Tuple

from django.contrib import auth
from django.db.models import QuerySet
from django.dispatch import receiver

from accounts.models import CustomUser, FriendRequest

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from accounts.utils import accounts_verify_token
from django.utils.encoding import force_bytes, force_str


def create_single_user(email: str, nickname: str, password: str, **kwargs: str) -> CustomUser:
    user = CustomUser.objects.create_user(email=email, nickname=nickname, password=password, **kwargs)
    return user


def check_email_duplication(email: str) -> bool:
    return CustomUser.objects.filter(email__iexact=email).exists()


def send_email_verification(user: CustomUser, current_domain: str) -> int:
    
    message = render_to_string(
        template_name='accounts/verification_email.html',
        context={
            'user':user,
            'domain':current_domain,
            'uid':urlsafe_base64_encode(force_bytes(user.id)).encode().decode(),
            'token':accounts_verify_token.make_token(user),
        }
    )

    mail_title = "[alaltalk] 이메일 인증 링크입니다."
    user_email = user.email
    email_message = EmailMessage(mail_title, message, to=[user_email])
    result = email_message.send()
    return result

def verified_email_activation(uidb64:str, token:str) -> None:
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user != None and accounts_verify_token.check_token(user=user, token=token):
        user.is_active = True
        user.save()

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


def accounts_profile_delete(user_id: int) -> None:
    CustomUser.objects.filter(id=user_id).delete()


def accounts_delete_friend(user_id: int, friend_id: int) -> None:
    user = CustomUser.objects.filter(id=user_id).get()
    friend = CustomUser.objects.filter(id=friend_id).get()    
    user.friends.remove(friend)
    friend.friends.remove(user)
    
    
