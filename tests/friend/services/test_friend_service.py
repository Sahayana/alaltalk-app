import pytest
from django.db import IntegrityError

from apps.friend import constants
from apps.friend.models import Friend
from apps.friend.services.friend_service import FriendService
from tests.account.factories import UserFactory
from tests.friend.factories import FriendFactory, FriendRequestFactory

pytestmark = pytest.mark.django_db


def test_친구_요청_전송():

    user = UserFactory.create()
    target_user = UserFactory.create()

    friend_request = FriendService.send_friend_request(
        user_id=user.id, target_user_id=target_user.id
    )

    assert friend_request.user.id == user.id
    assert friend_request.target_user.id == target_user.id
    assert friend_request.status == constants.FriendRequestStatus.SENT


def test_친구_요청_중복시_IntegrityError_발생():

    user = UserFactory.create()
    target_user = UserFactory.create()

    FriendService.send_friend_request(user_id=user.id, target_user_id=target_user.id)

    with pytest.raises(IntegrityError):
        FriendService.send_friend_request(
            user_id=user.id, target_user_id=target_user.id
        )


def test_친구_요청_승낙시_Friend_레코드_생성():

    target_user = UserFactory.create()
    friend_request = FriendRequestFactory.create(target_user=target_user)

    friend = FriendService.accpet_friend_request(
        target_user_id=target_user.id, request_id=friend_request.id
    )

    assert friend.target_user.friends.count() == 1
    assert friend.user.friends.count() == 1
    assert target_user.id in [user.id for user in friend.user.friends.all()]
    assert friend.user.id in [user.id for user in friend.target_user.friends.all()]
    assert friend.status == constants.FriendStatus.CONNECTED


def test_친구_요청_승낙시_FriendRequest_status_및_targetuser_accept_at_필드_업데이트():

    friend_request = FriendRequestFactory.create()

    FriendService.accpet_friend_request(
        target_user_id=friend_request.target_user.id, request_id=friend_request.id
    )

    # 해당 레코드를 다시 select해야함
    friend_request.refresh_from_db()

    assert friend_request.status == constants.FriendRequestStatus.ACCEPT
    assert friend_request.targetuser_accept_at is not None


def test_친구_요청_거절시_status_변경():

    target_user = UserFactory.create()
    friend_request = FriendRequestFactory.create(target_user=target_user)

    FriendService.decline_friend_request(
        target_user_id=target_user.id, request_id=friend_request.id
    )

    # 업데이트 메서드는 refresh_from_db 필요
    friend_request.refresh_from_db()

    assert friend_request.status == constants.FriendRequestStatus.DECLINE


def test_친구_상태_해제시_friend_레코드_status_변경_및_유저_친구_목록에서_삭제():

    user = UserFactory.create()
    target_user = UserFactory.create()
    friend_request = FriendRequestFactory.create(user=user, target_user=target_user)

    assert user.friends.count() == 0
    assert target_user.friends.count() == 0

    FriendService.accpet_friend_request(
        target_user_id=target_user.id, request_id=friend_request.id
    )

    assert user.friends.count() == 1
    assert target_user.friends.count() == 1

    friend = FriendService.disconnect_friend(
        user_id=user.id, target_user_id=target_user.id
    )

    assert friend.status == constants.FriendStatus.DISCONNECTED
