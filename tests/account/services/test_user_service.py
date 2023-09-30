import pytest
from django.contrib.auth.hashers import check_password
from django.core import mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.account.constants import EMAIL_VERIFY_TITLE
from apps.account.services.user_service import UserService
from apps.account.tasks import send_email_verification
from apps.account.utils import accounts_verify_token
from tests.account.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_인증_이메일_발송() -> None:

    user = UserFactory.create()

    send_email_verification(user_id=user.id)

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == EMAIL_VERIFY_TITLE


def test_유저_생성_서비스() -> None:
    email = "alaltalk_test"
    password = "alaltalk!"
    nickname = "alaltalk"
    bio = "alaltalk!"

    user = UserService.create_single_user(
        email=email, password=password, nickname=nickname, bio=bio
    )

    assert user is not None
    assert user.email == email
    assert user.bio == bio
    assert check_password(password, user.password) is True


def test_유저_이메일_인증_후_유저_상태_active_변경():

    user = UserFactory.create()
    send_email_verification(user_id=user.id)

    uidb64 = urlsafe_base64_encode(force_bytes(user.id)).encode().decode()
    token = accounts_verify_token.make_token(user)

    user = UserService.verified_email_activation(uidb64=uidb64, token=token)

    assert user.is_active is True


def test_존재하지않는_유저_이메일_인증_시도_None_반환():

    invalid_id = 999999
    user = UserFactory.create()

    uidb64 = urlsafe_base64_encode(force_bytes(invalid_id)).encode().decode()
    token = accounts_verify_token.make_token(user)

    user = UserService.verified_email_activation(uidb64=uidb64, token=token)

    assert user is None
