from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.friend import constants
from apps.friend.models import Friend, FriendRequest


class FriendService:
    @classmethod
    def send_friend_request(cls, user_id: int, target_user_id: int) -> FriendRequest:
        """
        친구 요청을 전송합니다.
        """
        try:
            friend_request = FriendRequest.objects.create(
                user_id=user_id,
                target_user_id=target_user_id,
                user_request_at=timezone.now(),
            )
        except IntegrityError:
            raise ValueError("이미 존재하는 요청입니다.")

        return friend_request

    @classmethod
    @transaction.atomic
    def accpet_friend_request(cls, target_user_id: int, request_id: int) -> Friend:
        """
        user의 친구 요청을 targetUser가 승낙하고 Friend 레코드를 생성합니다.
        """
        friend_request = FriendRequest.objects.select_related(
            "user", "target_user"
        ).get(id=request_id)

        if friend_request.target_user.id == target_user_id:
            try:
                friend = Friend.objects.create(
                    user_id=friend_request.user.id,
                    target_user_id=friend_request.target_user.id,
                )

                friend_request.status = constants.FriendRequestStatus.ACCEPT
                friend_request.targetuser_accept_at = timezone.now()
                friend_request.save()
            except IntegrityError:
                raise ValueError("이미 친구인 상태입니다.")
            return friend

    @classmethod
    def decline_friend_request(cls, request_id: int) -> None:
        """
        user의 친구 요청을 거절합니다.
        FriendRequest의 status를 DECLINE으로 변경합니다.
        """
        FriendRequest.objects.filter(id=request_id).update(
            status=constants.FriendRequestStatus.DECLINE
        )

    @classmethod
    def disconnect_friend(cls, user_id: int, target_user_id: int) -> Friend:
        """
        친구 상태를 해제합니다.
        """
        friend = Friend.objects.get(user_id=user_id, target_user_id=target_user_id)
        friend.status = constants.FriendStatus.DISCONNECTED
        friend.save()
        return friend
