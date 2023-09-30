from typing import Callable

import pytest
from django.core.files.base import File

from apps.account.constants import DEFAULT_IMG, EMAIL_DUPLICATION_MESSAGE, TEST_IMG_NAME
from apps.account.v1.serializers.user_serializer import (
    UserCreateSerializer,
    UserReadSerializer,
)
from tests.account.factories import UserFactory, UserProfileImageFactory

pytestmark = pytest.mark.django_db


def test_유저_생성_시리얼라이저_validated_data_반환(create_user_data: Callable):

    singed_user = UserFactory.build()
    data = create_user_data(singed_user)

    serializer = UserCreateSerializer(data=data)

    assert serializer.is_valid() is True
    assert serializer.validated_data == data


def test_유저_생성_시리얼라이저_프로필_이미지_설정_validated_data_반환(
    create_user_data: Callable, get_test_image: File
):

    signed_user = UserFactory.build()

    data = create_user_data(signed_user)
    data.update({"profile_image": get_test_image})

    serializer = UserCreateSerializer(data=data)

    assert serializer.is_valid() is True
    assert serializer.validated_data == data
    assert serializer.validated_data["profile_image"].name == TEST_IMG_NAME


def test_유저_조회_시리얼라이저_validated_data_반환():

    user = UserFactory.create()
    serializer = UserReadSerializer(instance=user)
    data = serializer.data

    assert data["id"] == user.id
    assert data["email"] == user.email
    assert data["nickname"] == user.nickname
    assert data["bio"] == user.bio


def test_유저_조회_시리얼라이저_이미지_없을시_기본이미지_반환():

    user = UserFactory.create()
    serializer = UserReadSerializer(instance=user)
    data = serializer.data

    assert data["profile_image"] == DEFAULT_IMG


def test_유저_조회_시리얼라이저_이미지_있을시_이미지_반환():

    user = UserFactory.create()
    profile_image = UserProfileImageFactory.create(user=user)

    serializer = UserReadSerializer(instance=user)
    data = serializer.data

    assert data["profile_image"] == profile_image.img
