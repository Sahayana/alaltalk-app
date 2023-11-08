from typing import Callable

import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status

from apps.account.models import UserLikeKeyWord
from apps.friend import constants
from apps.friend.models import Friend
from apps.friend.v1.apis.friend_api import FriendViewSet
from tests.account.factories import UserFactory, UserLikeKeywordFactory
from tests.friend.factories import FriendFactory
from tests.helpers import authorization_header
from tests.search.factories import (
    BookFactory,
    NewsFactory,
    ShoppingFactory,
    YoutubeFactory,
)

pytestmark = pytest.mark.django_db

view = FriendViewSet()


def test_친구_해제시_deleted_메시지_및_상태_변경_반환(client: Client):

    user = UserFactory.create(is_active=True)
    target_user = UserFactory.create(is_active=True)

    friend = FriendFactory.create(user=user, target_user=target_user)

    res = client.delete(
        f"/friend/v1/friends/{friend.id}/",
        **authorization_header(user),
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data["msg"] == "deleted"
    assert (
        Friend.objects.get(id=friend.id).status == constants.FriendStatus.DISCONNECTED
    )


def test_관심_키워드_저장_add_like_메시지_및_유저라이크키워드_데이터_반환(client: Client):

    user = UserFactory.create(is_active=True)
    keyword = "test"

    data = {"like_keyword": keyword}

    res = client.post(
        reverse("friend:v1:friends-keyword"),
        data=data,
        content_type="application/json",
        **authorization_header(user),
    )

    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["msg"] == "add like"
    assert res.data["data"]["keyword"] == keyword


def test_관심_키워드_최대_3개_노출(client: Client):

    user = UserFactory.create(is_active=True)
    target_user = UserFactory.create(is_active=True)

    sample_keywords = ["test1", "test2", "test3", "test4", "test5"]

    for word in sample_keywords:
        UserLikeKeywordFactory.create(user=target_user, keyword=word)

    data = {"target_user_id": target_user.id}

    res = client.post(
        reverse("friend:v1:friends-recommend-keywords"),
        data=data,
        content_type="application/json",
        **authorization_header(user),
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data["keywords"] == list(reversed(sample_keywords))[:3]


def test_유저_좋아요_데이터_like_sentence_반환(client: Client):

    user = UserFactory.create(is_active=True)
    youtube = YoutubeFactory.create(user=user)
    news = NewsFactory.create(user=user)
    book = BookFactory.create(user=user)
    shopping = ShoppingFactory.create(user=user)

    res = client.post(
        reverse("friend:v1:friends-get-user-like"),
        content_type="application/json",
        **authorization_header(user),
    )

    sentence = (
        youtube.title + " " + news.title + " " + book.title + " " + shopping.title + " "
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data["like_sentence"] == sentence
