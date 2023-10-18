from rest_framework import serializers

from apps.account.constants import DEFAULT_IMG, EMAIL_DUPLICATION_MESSAGE
from apps.account.models import CustomUser, UserLikeKeyWord, UserProfileImage
from apps.account.services.user_selector import UserSelector


class UserCreateSerializer(serializers.ModelSerializer):

    email = serializers.CharField(required=True)
    nickname = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ("email", "password", "nickname", "bio", "profile_image")


class UserReadSerializer(serializers.ModelSerializer):

    profile_image = serializers.SerializerMethodField()

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

    def get_profile_image(self, obj):

        profile_img = UserProfileImage.objects.filter(user_id=obj.id).first()
        if not profile_img:
            return DEFAULT_IMG
        return profile_img.img


class UserLikeKeywordSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = UserLikeKeyWord
        fields = "__all__"
