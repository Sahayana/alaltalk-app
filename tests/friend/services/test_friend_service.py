import pytest
from django.db import IntegrityError

from apps.friend import constants
from apps.friend.models import Friend
from apps.friend.services.friend_service import FriendService
from tests.account.factories import UserFactory, UserLikeKeywordFactory
from tests.friend.factories import FriendFactory, FriendRequestFactory
from tests.search.factories import (
    BookFactory,
    NewsFactory,
    ShoppingFactory,
    YoutubeFactory,
)

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

    friend = FriendService.accept_friend_request(
        target_user_id=target_user.id, request_id=friend_request.id
    )

    assert friend.target_user.friends.count() == 1
    assert friend.user.friends.count() == 1
    assert target_user.id in [user.id for user in friend.user.friends.all()]
    assert friend.user.id in [user.id for user in friend.target_user.friends.all()]
    assert friend.status == constants.FriendStatus.CONNECTED


def test_친구_요청_승낙시_FriendRequest_status_및_targetuser_accept_at_필드_업데이트():

    friend_request = FriendRequestFactory.create()

    FriendService.accept_friend_request(
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


def test_친구_상태_해제시_friend_레코드_status_변경():

    user = UserFactory.create()
    target_user = UserFactory.create()
    friend_request = FriendRequestFactory.create(user=user, target_user=target_user)

    assert user.friends.count() == 0
    assert target_user.friends.count() == 0

    FriendService.accept_friend_request(
        target_user_id=target_user.id, request_id=friend_request.id
    )

    assert user.friends.count() == 1
    assert target_user.friends.count() == 1

    friends_connections = FriendService.disconnect_friend(
        user_id=user.id, target_user_id=target_user.id
    )

    assert friends_connections[0].status == constants.FriendStatus.DISCONNECTED
    assert friends_connections[1].status == constants.FriendStatus.DISCONNECTED


def test_친구_추천_상위_5명_노출_확인(mocker):

    size = 5
    user = UserFactory.create()
    UserLikeKeywordFactory.create(user=user)

    similarity = [100, 80, 60, 40, 20]
    users = UserFactory.create_batch(size=size)
    mocking_value = {
        idx: simil for idx, (user, simil) in enumerate(zip(users, similarity))
    }
    mocker.patch(
        "apps.friend.services.friend_service.FriendService.get_keyword_similarity",
        return_value=mocking_value,
    )

    recommended = FriendService.recommend_friend(user=user)

    assert sorted([user.id for user in recommended]) == sorted(
        [user.id for user in users]
    )


def test_친구_관심_키워드_최신순_최대_3개_노출():

    friend = UserFactory.create()
    keywords = UserLikeKeywordFactory.create_batch(size=5, user=friend)
    keywords.reverse()

    recommended = FriendService.friend_like_recommend(target_user_id=friend.id)

    assert len(recommended) == 3
    assert [word for word in recommended] == [obj.keyword for obj in keywords[:3]]


def test_유저_like_데이터_불러오기():

    user = UserFactory.create()
    youtube = YoutubeFactory.create(user=user)
    news = NewsFactory.create(user=user)
    book = BookFactory.create(user=user)
    shopping = ShoppingFactory.create(user=user)

    sentence = FriendService.get_user_like_data(user_id=user.id)

    assert (
        sentence
        == youtube.title
        + " "
        + news.title
        + " "
        + book.title
        + " "
        + shopping.title
        + " "
    )
