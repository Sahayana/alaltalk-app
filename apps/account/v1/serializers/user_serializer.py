from rest_framework import serializers

from apps.account.models import CustomUser, UserProfileImage
from apps.account.v1.serializers.fields import ProfileImageField


class UserProfileImageSerialier(serializers.ModelSerializer):
    class Meta:
        model = UserProfileImage
        fields = ("id", "img")


class UserCreateSerializer(serializers.ModelSerializer):

    email = serializers.CharField(required=True)
    nickname = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    user_profile_imgs = UserProfileImageSerialier(required=False)

    class Meta:
        model = CustomUser
        fields = ("email", "nickname", "bio", "user_profile_imgs")


class UserReadSerializer(serializers.ModelSerializer):

    profile_image = ProfileImageField()

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "nickname",
            "bio",
            "date_joined",
            "last_login",
            "profile_image",
            "is_active",
            "is_recommend_on",
            "is_like_public",
        )
