from typing import Callable

import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status

from apps.account.constants import DEFAULT_IMG
from tests.account.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_유저_생성페이지_렌더링(client: Client):

    res = client.get(reverse("account:v1:signup"))

    assert res.status_code == status.HTTP_200_OK
    assert "account/signup.html" in [template.name for template in res.templates]


def test_유저_생성(client: Client, create_user_data: Callable):

    user = UserFactory.build()

    data = create_user_data(user)

    res = client.post(
        reverse("account:v1:signup"), data=data, content_type="application/json"
    )

    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["msg"] == "sent"
    assert res.data["user"]["email"] == user.email
    assert res.data["user"]["profile_image"] == DEFAULT_IMG
