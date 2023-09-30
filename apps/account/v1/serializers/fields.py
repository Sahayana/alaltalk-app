from rest_framework import serializers

from apps.account.constants import DEFAULT_IMG
from apps.account.models import CustomUser, UserProfileImage


class ProfileImageField(serializers.Field):

    """
    유저의 프로필 사진이 없는 경우 디폴트 이미지를 노출하는 시리얼라이저 필드입니다.
    """

    def to_representation(self, user: CustomUser):
        try:
            profile_img = UserProfileImage.objects.filter(user=user).first()
        except UserProfileImage.DoesNotExist:
            return DEFAULT_IMG
        finally:
            return profile_img

    def to_internal_value(self, data):
        return data
