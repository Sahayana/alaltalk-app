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


def test_현재_친구_목록_렌더링_및_템플릿_확인(client: Client):

    user = UserFactory.create(is_active=True)

    res = client.get(reverse("friend:v1:friends-list"), **authorization_header(user))

    assert res.status_code == status.HTTP_200_OK
    assert "account/user_list.html" in [template.name for template in res.templates]


def test_친구_목록_조회시_현재_친구유저_추천친구에_불포함(client: Client):

    user = UserFactory.create(is_active=True)
    target_users = UserFactory.create_batch(size=5, is_active=True)

    friends = []
    for target_user in target_users:
        friends.append(FriendFactory.create(user=user, target_user=target_user))

    res = client.get(reverse("friend:v1:friends-list"), **authorization_header(user))

    assert res.status_code == status.HTTP_200_OK
    assert sorted([friend.id for friend in res.data["friends"]]) == sorted(
        [friend.id for friend in friends]
    )
    assert len(res.data["recommend_friend"]) == 0


def test_친구_목록_조회시_현재친구_및_추천친구_최대_5명_반환(client: Client):

    user = UserFactory.create(is_active=True)
    target_users = UserFactory.create_batch(size=10, is_active=True)

    friends = []
    for target_user in target_users[:5]:
        friends.append(FriendFactory.create(user=user, target_user=target_user))

    res = client.get(reverse("friend:v1:friends-list"), **authorization_header(user))

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data["recommend_friend"]) == 5
    assert sorted([friend.id for friend in res.data["friends"]]) == sorted(
        [friend.id for friend in friends]
    )


def test_유저_검색시_이메일_혹은_닉네임_동시_검색_확인(client: Client):

    email = "searchtest@alaltalk.com"
    nickname = "searchtest"

    query = "search"

    user = UserFactory.create(is_active=True)
    email_target_user = UserFactory.create(email=email, is_active=True)
    nickname_target_user = UserFactory.create(nickname=nickname, is_active=True)

    res = client.get(
        reverse("friend:v1:friends-search") + f"?q={query}",
        **authorization_header(user),
    )

    assert res.status_code == status.HTTP_200_OK
    assert len(list(res.data["result"])) == 2
    assert res.data["result"][0]["email"] == email_target_user.email
    assert res.data["result"][1]["email"] == nickname_target_user.email
