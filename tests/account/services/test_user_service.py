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


def test_유저_관심_키워드_저장():

    user = UserFactory.create()
    keyword = "python"
    like_keyworkd = UserService.save_like_keyword(user_id=user.id, keyword=keyword)

    assert like_keyworkd.keyword == keyword


def test_유저_좋아요_컨텐츠_노출_off_변경시_필드_변경():

    user = UserFactory.create()
    value = "OFF"

    user = UserService.like_public_setting(user_id=user.id, value=value)

    assert user.is_like_public is False


def test_유저_탙퇴시_is_deleted_필드값_변경():

    user = UserFactory.create(is_active=True)
    deleted_user = UserService.delete_user_account(user_id=user.id)

    assert deleted_user.is_deleted is True


def test_유저_임시비밀번호_발송_비밀번호_체크_확인(mocker):

    user = UserFactory.create(is_active=True)
    temp_str = "temporary"

    mocker.patch(
        "apps.account.services.user_service.random_string_generator",
        return_value=temp_str,
    )

    after_user = UserService.change_temporary_password(user_id=user.id)

    assert after_user.check_password(temp_str) is True
