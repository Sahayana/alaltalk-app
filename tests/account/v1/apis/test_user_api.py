from typing import Callable

import pytest
from django.core import mail
from django.test import Client
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status

from apps.account.constants import DEFAULT_IMG, EMAIL_VERIFY_TITLE
from apps.account.services.user_service import UserService
from apps.account.utils import accounts_verify_token
from tests.account.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_유저_생성페이지_렌더링(client: Client):

    res = client.get(reverse("account:v1:signup"))

    assert res.status_code == status.HTTP_200_OK
    assert "account/signup.html" in [template.name for template in res.templates]


@pytest.mark.django_db(transaction=True)
def test_유저_생성(
    client: Client, create_user_data: Callable, django_capture_on_commit_callbacks
):

    user = UserFactory.build()

    data = create_user_data(user)

    with django_capture_on_commit_callbacks(execute=True):
        res = client.post(
            reverse("account:v1:signup"), data=data, content_type="application/json"
        )

        assert res.status_code == status.HTTP_201_CREATED
        assert res.data["msg"] == "sent"
        assert res.data["user"]["email"] == user.email
        assert res.data["user"]["profile_image"] == DEFAULT_IMG
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == EMAIL_VERIFY_TITLE


def test_유저_인증_성공시_status_user_반환(client: Client):

    user = UserFactory.create()
    UserService._send_email_verification(user=user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.id)).encode().decode()
    token = accounts_verify_token.make_token(user)

    res = client.get(
        reverse("account:v1:user_activation", kwargs={"uidb64": uidb64, "token": token})
    )

    assert res.status_code == status.HTTP_202_ACCEPTED
    assert res.data["msg"] == "activated"
    assert res.data["user"]["is_active"] is True
    assert res.data["user"]["email"] == user.email


def test_유저_인증_실패시_인증실패_메시지_반환(client: Client):

    user = UserFactory.create()
    UserService._send_email_verification(user=user)
    uidb64 = "INVALID"
    token = accounts_verify_token.make_token(user)

    res = client.get(
        reverse("account:v1:user_activation", kwargs={"uidb64": uidb64, "token": token})
    )

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert res.data["msg"] == "not_activated"


def test_로그인_페이지_렌더링(client: Client):

    res = client.get(reverse("account:v1:login"))

    assert res.status_code == status.HTTP_200_OK
    assert "account/login.html" in [template.name for template in res.templates]


def test_로그인_성공시_access_token_반환(client: Client):

    email = "test@alaltalk.com"
    password = "alaltalk!"

    user = UserFactory.create(email=email, password=password)
    user.is_active = True
    user.save()

    data = {"email": email, "password": password}

    res = client.post(
        reverse("account:v1:login"), data=data, content_type="application/json"
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data is not None
