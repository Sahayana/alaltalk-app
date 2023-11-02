import pytest

from apps.friend import constants
from apps.friend.v1.serializers.friend_serializer import FriendRequestSerializer
from tests.friend.factories import FriendRequestFactory

pytestmark = pytest.mark.django_db


def test_friend_request_seriliazer_조회시_유효한_데이터_반환():

    friend_request = FriendRequestFactory.create()
    serializer = FriendRequestSerializer(instance=friend_request)
    data = serializer.data

    assert data["user"]["email"] == friend_request.user.email
    assert data["target_user"]["email"] == friend_request.target_user.email
    assert data["status"] == constants.FriendRequestStatus.SENT
