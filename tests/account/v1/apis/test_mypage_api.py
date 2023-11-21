import io

import pytest
from django.core import mail
from django.core.files.base import ContentFile
from django.test import Client
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.urls import reverse
from PIL import Image
from rest_framework import status

from apps.account.models import UserProfileImage
from tests.account.factories import UserFactory, UserProfileImageFactory
from tests.friend.factories import FriendRequestFactory
from tests.helpers import authorization_header
from tests.search.factories import (
    BookFactory,
    NewsFactory,
    ShoppingFactory,
    YoutubeFactory,
)

pytestmark = pytest.mark.django_db


def test_등록되지_않은_유저_마이페이지_접근시_401에러_발생(client: Client):

    res = client.get(reverse("account:v1:mypage-list"))

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_active_인증_받지_않은_유저_접근시_401에러_발생(client: Client):

    user = UserFactory.create(is_active=False)

    res = client.get(reverse("account:v1:mypage-list"), **authorization_header(user))

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_유저_마이페이지_템플릿_렌더링_확인(client: Client):

    user = UserFactory.create(is_active=True)

    res = client.get(reverse("account:v1:mypage-list"), **authorization_header(user))

    assert res.status_code == status.HTTP_200_OK
    assert "account/mypage.html" in [template.name for template in res.templates]


def test_유저_마이페이지_유저_정보_및_받은_친구_요청_반환(client: Client):

    user = UserFactory.create(is_active=True)
    friends_requests = FriendRequestFactory.create_batch(size=10, target_user=user)

    res = client.get(reverse("account:v1:mypage-list"), **authorization_header(user))

    assert res.status_code == status.HTTP_200_OK
    assert res.data["user"].email == user.email
    assert len(res.data["friend_requests"]) == len(friends_requests)


def test_유저_마이페이지_유튜브_뉴스_책_쇼핑_데이터_반환(client: Client):

    user = UserFactory.create(is_active=True)
    size = 5

    youtubes = YoutubeFactory.create_batch(size=size, user=user)
    news = NewsFactory.create_batch(size=size, user=user)
    books = BookFactory.create_batch(size=size, user=user)
    shoppings = ShoppingFactory.create_batch(size=size, user=user)

    res = client.get(reverse("account:v1:mypage-list"), **authorization_header(user))

    assert res.status_code == status.HTTP_200_OK
    assert res.data["user"].email == user.email
    assert len(res.data["youtubes"]) == len(youtubes)
    assert len(res.data["news"]) == len(news)
    assert len(res.data["books"]) == len(books)
    assert len(res.data["shoppings"]) == len(shoppings)
    assert sorted([obj.id for obj in res.data["youtubes"]]) == sorted(
        [obj.id for obj in youtubes]
    )
    assert sorted([obj.id for obj in res.data["news"]]) == sorted(
        [obj.id for obj in news]
    )
    assert sorted([obj.id for obj in res.data["books"]]) == sorted(
        [obj.id for obj in books]
    )
    assert sorted([obj.id for obj in res.data["shoppings"]]) == sorted(
        [obj.id for obj in shoppings]
    )


def test_유저_회원정보_이미지_제외한_정보_업데이트(client: Client):

    user = UserFactory.create(is_active=True)

    nickname = "updated"

    data = {"nickname": nickname}

    res = client.post(
        reverse("account:v1:mypage-list"),
        **authorization_header(user),
        data=data,
        media_type="multipart/form-data"
    )

    res_data = res.data["data"]

    assert res.status_code == status.HTTP_200_OK
    assert res.data["msg"] == "ok"
    assert res_data["nickname"] == nickname
    assert res_data["email"] == user.email
    assert res_data["bio"] == user.bio


def test_유저_회원정보_프로필_이미지_업데이트_확인(client: Client):

    user = UserFactory.create(is_active=True)
    user_img = UserProfileImageFactory.create()

    data = {"profile_image": user_img.img, "bio": "test"}

    res = client.post(
        reverse("account:v1:mypage-list"),
        **authorization_header(user),
        data=data,
        media_type="multipart/form-data"
    )

    res_data = res.data["data"]

    assert res.status_code == status.HTTP_200_OK
    assert res.data["msg"] == "ok"
    assert UserProfileImage.objects.filter(user=user).exists() is True
    assert res_data["nickname"] == user.nickname
    assert res_data["email"] == user.email
    assert res_data["bio"] == "test"
