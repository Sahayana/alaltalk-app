import datetime
from typing import Tuple

import jwt
from accounts.models import CustomUser, FriendRequest
from accounts.utils import FriendType, accounts_verify_token
from django.core.mail import EmailMessage
from django.db.models import Q, QuerySet
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from alaltalk.settings import SECRET_KEY


def create_single_user(
    email: str, nickname: str, password: str, **kwargs: str
) -> CustomUser:
    user = CustomUser.objects.create_user(
        email=email, nickname=nickname, password=password, **kwargs
    )
    return user


def check_email_duplication(email: str) -> bool:
    return CustomUser.objects.filter(email__iexact=email).exists()


def send_email_verification(user: CustomUser, current_domain: str) -> int:

    message = render_to_string(
        template_name="accounts/verification_email.html",
        context={
            "user": user,
            "domain": current_domain,
            "uid": urlsafe_base64_encode(force_bytes(user.id)).encode().decode(),
            "token": accounts_verify_token.make_token(user),
        },
    )

    mail_title = "[alaltalk] 이메일 인증 링크입니다."
    user_email = user.email
    email_message = EmailMessage(mail_title, message, to=[user_email])
    result = email_message.send()
    return result


def verified_email_activation(uidb64: str, token: str) -> None:
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and accounts_verify_token.check_token(user=user, token=token):
        user.is_active = True
        user.save()


def get_friend_list(user_id: int) -> QuerySet[CustomUser]:
    user = CustomUser.objects.get(id=user_id)
    friends = user.friends.all()
    return friends


def send_friend_request(sender_id: int, recevier_id: int) -> Tuple[CustomUser, bool]:
    friend_request, is_created = FriendRequest.objects.get_or_create(
        sender_id=sender_id, receiver_id=recevier_id
    )
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
    authenticated = user.check_password(password)
    return authenticated


def accounts_profile_delete(user_id: int) -> None:
    CustomUser.objects.filter(id=user_id).delete()


def accounts_delete_friend(user_id: int, friend_id: int) -> None:
    user = CustomUser.objects.filter(id=user_id).get()
    friend = CustomUser.objects.filter(id=friend_id).get()
    user.friends.remove(friend)
    friend.friends.remove(user)


def accounts_token_authenticated(user_email: str, user_password: str):

    try:
        user = CustomUser.objects.get(email=user_email)
        if not user.is_active:
            return "NOT_ACTIVATED"
        elif user.check_password(user_password):
            payload = {
                "email": user.email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60 * 24),
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            token = token.decode("utf-8")
            return token
        else:
            return "UNVALID_PASSWORD"
    except CustomUser.DoesNotExist:
        return "NOT_REGISTERD"


def accounts_search_friends(user_id: int, query: str):

    me = CustomUser.objects.prefetch_related("friends").get(
        id=user_id
    )  # total num of query = 2
    search_users = list(
        CustomUser.objects.filter(
            Q(email__icontains=query) | Q(nickname__icontains=query)
        ).distinct()
    )  # total num of query = 3

    if len(search_users) == 0:
        return {"message": "NONE"}

    for i, user in enumerate(search_users):
        if user in me.friends.all():
            search_users[i] = (user, FriendType.is_friend.value)
        elif user.id == me.id:
            search_users[i] = (user, FriendType.is_self.value)
        else:
            search_users[i] = (user, FriendType.is_not_friend.value)
    return search_users
