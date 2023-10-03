from django.db import models

from apps.account.models import CustomUser
from apps.base_model import BaseModel
from apps.friend import constants


class FriendRequest(BaseModel):

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="friend_request_user"
    )
    target_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="friend_request_targetuser"
    )
    status = models.PositiveSmallIntegerField(
        choices=constants.FriendRequestStatus.choices, default=0
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


class Friend(BaseModel):

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="friends_user"
    )
    target_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="friends_targetuser"
    )
    status = models.PositiveSmallIntegerField(
        choices=constants.FriendStatus.choices, default=0
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "target_user"], name="unique_friend"
            )
        ]
