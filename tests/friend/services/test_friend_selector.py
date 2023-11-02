import pytest

from apps.friend.services.friend_selector import FriendSelector
from tests.account.factories import UserFactory
from tests.friend.factories import FriendFactory, FriendRequestFactory

pytestmark = pytest.mark.django_db


def test_받은_친구_요청_조회():

    target_user = UserFactory.create()
    size = 5
    FriendRequestFactory.create_batch(size=size, target_user=target_user)

    recieved_requests = FriendSelector.get_recieved_requests(user_id=target_user.id)

    assert [target_user.id for _ in range(size)] == [
        request.target_user.id for request in recieved_requests
    ]


def test_내가_보낸_친구_요청_조회():

    user = UserFactory.create()
    size = 5
    requests = FriendRequestFactory.create_batch(size=size, user=user)

    sent_requests = FriendSelector.get_sent_requests(user_id=user.id)

    assert [user.id for _ in range(size)] == [
        request.user.id for request in sent_requests
    ]
    assert [request.target_user.id for request in reversed(requests)] == [
        request.target_user.id for request in sent_requests
    ]


def test_현재_친구_목록_order_by_조회_확인():

    user = UserFactory.create()
    size = 5
    friends = FriendFactory.create_batch(size=size, user=user)
    friends.sort(key=lambda friend: friend.target_user.nickname, reverse=True)

    current_friends = FriendSelector.get_friends_list(user_id=user.id)

    assert len(friends) == len(current_friends)
    assert friends == list(current_friends)


def test_친구_검색_email_nickname_같아도_distinct_확인():

    user = UserFactory.create()
    email = "newuser@alaltlak.com"
    nickname = "newuser"
    new_user = UserFactory.create(email=email, nickname=nickname)

    query = "newuser"
    users = FriendSelector.search_friend(user_id=user.id, query=query)

    assert users.count() == 1
    assert users[0].email == new_user.email
