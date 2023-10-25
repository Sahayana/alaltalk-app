from typing import Callable

import pytest
from django.db import IntegrityError
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.friend import constants
from apps.friend.models import Friend, FriendRequest
from tests.account.factories import UserFactory
from tests.friend.factories import FriendFactory, FriendRequestFactory
from tests.helpers import authorization_header

pytestmark = pytest.mark.django_db


def test_친구_요청시_유효하지않은_토큰_인증_오류_반환(client: Client):

    token = "invalid_token"

    user, target_user = UserFactory.create_batch(size=2)

    data = {"user": user.id, "target_user": target_user.id}
    res = client.post(
        reverse("friend:v1:friend_request-list"),
        data=data,
        content_type="application/json",
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_친구_요청시_sent_메시지_및_데이터_반환(client: Client, mocker: Callable):

    now = timezone.now()
    mocker.patch("django.utils.timezone.now", return_value=now)

    user = UserFactory.create(is_active=True)
    target_user = UserFactory.create(is_active=True)

    data = {"user": user.id, "target_user": target_user.id}

    res = client.post(
        reverse("friend:v1:friend_request-list"),
        data=data,
        content_type="application/json",
        **authorization_header(user),
    )

    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["msg"] == "sent"
    assert res.data["data"]["user"]["email"] == user.email
    assert res.data["data"]["target_user"]["email"] == target_user.email
    assert res.data["data"]["status"] == constants.FriendRequestStatus.SENT
    assert (
        FriendRequest.objects.filter(user=user, target_user=target_user).exists()
        is True
    )


def test_친구_요청_중복시_already_메시지_반환(client: Client):
    user = UserFactory.create(is_active=True)
    target_user = UserFactory.create(is_active=True)
    FriendRequestFactory.create(user=user, target_user=target_user)

    data = {"user": user.id, "target_user": target_user.id}

    res = client.post(
        reverse("friend:v1:friend_request-list"),
        data=data,
        content_type="application/json",
        **authorization_header(user),
    )

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert res.data["msg"] == "already"


def test_친구_요청_승낙시_status_변경_및_Friend_레코드_생성_확인(client: Client):
    user = UserFactory.create(is_active=True)
    target_user = UserFactory.create(is_active=True)
    friend_request = FriendRequestFactory.create(user=user, target_user=target_user)

    res = client.get(
        f"/friend/v1/friend_request/{friend_request.id}/",
        **authorization_header(target_user),
    )

    friend = Friend.objects.filter(user=user, target_user=target_user).get()

    assert res.status_code == status.HTTP_200_OK
    assert (
        FriendRequest.objects.get(user=user, target_user=target_user).status
        == constants.FriendRequestStatus.ACCEPT
    )
    assert friend.status == constants.FriendStatus.CONNECTED


def test_친구_요청_승낙시_user_및_targetUser_친구_확인(client: Client):
    user = UserFactory.create(is_active=True)
    target_user = UserFactory.create(is_active=True)
    friend_request = FriendRequestFactory.create(user=user, target_user=target_user)

    res = client.get(
        f"/friend/v1/friend_request/{friend_request.id}/",
        **authorization_header(target_user),
    )
    friend = Friend.objects.filter(user=user, target_user=target_user).get()

    assert res.status_code == status.HTTP_200_OK
    assert target_user in friend.user.friends.all()
    assert user in friend.target_user.friends.all()


def test_친구_상태에서_다시_친구_요청_승낙시_IntegrityError_발생(client: Client):
    user = UserFactory.create(is_active=True)
    target_user = UserFactory.create(is_active=True)
    friend_request = FriendRequestFactory.create(user=user, target_user=target_user)
    FriendFactory.create(user=user, target_user=target_user)

    with pytest.raises(IntegrityError):
        client.get(
            f"/friend/v1/friend_request/{friend_request.id}/",
            **authorization_header(target_user),
        )
