import pytest

from apps.account.services.user_selector import UserSelector
from tests.account.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_유저_이메일_중복_확인():

    user = UserFactory.create()
    is_duplicated = UserSelector().check_email_duplication(email=user.email)

    assert is_duplicated is True


def test_유저_단건_조회():

    new_user = UserFactory.create()
    user = UserSelector().get_user_by_id(user_id=new_user.id)

    assert user.id == new_user.id
    assert user.email == new_user.email


def test_없는_유저_조회시_None_반환():

    invalid_id = 99999
    user = UserSelector().get_user_by_id(user_id=invalid_id)

    assert user is None
