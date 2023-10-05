from django.conf import settings
from django.db import models

from apps.base_model import BaseModel
from apps.friend import constants


class FriendRequest(BaseModel):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_friend_requests",
    )
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="targetuser_friend_requests",
    )
    status = models.PositiveSmallIntegerField(
        choices=constants.FriendRequestStatus.choices,
        default=constants.FriendRequestStatus.SENT,
    )
    user_requested_at = models.DateTimeField(null=True, verbose_name="user_request_at")
    targetuser_accept_at = models.DateTimeField(
        null=True, blank=True, verbose_name="targetuser_accept_at"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "target_user"], name="unique_friend_request"
            )
        ]

    def __str__(self) -> str:
        return (
            f"Friend request from {self.user.nickname} to {self.target_user.nickname}"
        )


class Friend(BaseModel):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_friends"
    )
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="targetuser_friends",
    )
    status = models.PositiveSmallIntegerField(
        choices=constants.FriendStatus.choices, default=constants.FriendStatus.CONNECTED
    )

    def __str__(self) -> str:
        return f"Friend connection between {self.user.nickname} and {self.target_user.nickname}"
