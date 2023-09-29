import pytest
from django.contrib.auth.hashers import check_password
from django.core import mail

from apps.account.constants import EMAIL_VERIFY_TITLE
from apps.account.services.user_service import UserService
from tests.account.factories import UserFactory

pytestmark = pytest.mark.django_db


# TODO: 이메일 인증 API 완성 후 테스트
# def test_인증_이메일_발송() -> None:

#     user = UserFactory.build()

#     UserService._send_email_verification(user=user)

#     assert len(mail.outbox) == 1
#     assert mail.outbox[0].subject == EMAIL_VERIFY_TITLE


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
