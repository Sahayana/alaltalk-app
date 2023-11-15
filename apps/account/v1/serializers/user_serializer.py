from rest_framework import serializers

from apps.account.constants import DEFAULT_IMG, EMAIL_DUPLICATION_MESSAGE
from apps.account.models import CustomUser, UserLikeKeyWord, UserProfileImage
from apps.account.services.user_selector import UserSelector


class UserProfileImageSerializer(serializers.Serializer):
    profile_image = serializers.ImageField(write_only=True)


class UserCreateSerializer(serializers.ModelSerializer):

    email = serializers.CharField(required=True)
    nickname = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    profile_image = serializers.ImageField(required=False, write_only=True)

    class Meta:
        model = CustomUser
        fields = ("email", "password", "nickname", "bio", "profile_image")


class UserUpdateSerializer(serializers.ModelSerializer):

    nickname = serializers.CharField(required=False)
    password = serializers.CharField(required=False, write_only=True)
    bio = serializers.CharField(required=False)
    profile_image = serializers.ImageField(required=False, write_only=True)

    class Meta:
        model = CustomUser
        fields = ("nickname", "password", "bio", "profile_image")

    def update(self, instance, validated_data):
        if validated_data.get("profile_image"):
            img = validated_data.pop("profile_image")
            UserProfileImage.objects.create(user_id=instance.id, img=img)

        return super().update(instance, validated_data)


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
            "is_deleted",
        )

    def get_profile_image(self, obj):

        profile_img = UserProfileImage.objects.filter(user_id=obj.id).first()
        if not profile_img:
            return DEFAULT_IMG
        return profile_img.img.url


class UserLikeKeywordSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = UserLikeKeyWord
        fields = "__all__"
