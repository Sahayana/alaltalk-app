from django.db.models import Q, QuerySet

from apps.account.models import CustomUser
from apps.friend import constants
from apps.friend.models import Friend, FriendRequest


class FriendSelector:
    @classmethod
    def get_recieved_requests(cls, user_id: int) -> QuerySet[FriendRequest]:
        """
        받은 친구 요청을 조회합니다.
        """
        return FriendRequest.objects.filter(
            target_user_id=user_id, status=constants.FriendRequestStatus.SENT
        ).order_by("-id")

    @classmethod
    def get_sent_requests(cls, user_id: int) -> QuerySet[FriendRequest]:
        """
        보낸 친구 요청을 조회합니다.
        """
        return FriendRequest.objects.filter(
            user_id=user_id, status=constants.FriendRequestStatus.SENT
        ).order_by("-id")

    @classmethod
    def get_recieved_requests_count(cls, user_id: int) -> int:
        """
        받은 친구 요청의 갯수를 조회합니다.
        """
        return cls.get_recieved_requests(user_id=user_id).count()

    @classmethod
    def get_sent_request_count(cls, user_id: int) -> int:
        """
        보낸 친구 요청의 갯수를 조회합니다.
        """
        return cls.get_sent_requests(user_id=user_id).count()

    @classmethod
    def get_friends_list(cls, user_id: int) -> QuerySet[Friend]:
        """
        현재 친구 목록을 조회합니다.
        """
        return (
            Friend.objects.select_related(
                "target_user", "target_user__user_profile_imgs"
            )
            .filter(user_id=user_id, status=constants.FriendStatus.CONNECTED)
            .order_by("-target_user__nickname")
        )

    @classmethod
    def search_friend(cls, user_id: int, query: str) -> QuerySet[CustomUser]:
        """
        query를 통해 받은 문자열로 유저 혹은 친구상태의 유저를 검색합니다.
        """
        users = (
            CustomUser.objects.filter(
                Q(email__istartswith=query) | Q(nickname__istartswith=query)
            )
            .exclude(id=user_id)
            .distinct()
        )
        return users
