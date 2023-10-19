from rest_framework import serializers

from apps.account.v1.serializers.user_serializer import UserReadSerializer
from apps.friend.models import FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    user = UserReadSerializer(read_only=True)
    target_user = UserReadSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = (
            "user",
            "target_user",
            "status",
            "user_requested_at",
            "targetuser_accept_at",
        )
