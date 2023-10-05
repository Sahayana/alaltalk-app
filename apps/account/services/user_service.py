from django.db import transaction
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from apps.account.models import CustomUser, UserLikeKeyWord, UserProfileImage
from apps.account.tasks import send_email_verification
from apps.account.utils import accounts_verify_token


class UserService:
    @classmethod
    @transaction.atomic()
    def create_single_user(
        cls, email: str, nickname: str, bio: str, password: str, img=None
    ) -> CustomUser:
        """
        새로운 유저를 생성합니다.
        img 인자값이 들어오면 UserProfileImage 레코드를 생성하고 유저의 프로필 이미지로 저장합니다.

        param
        ------
        email, nickname, bio, password, img(Optional)
        """

        user = CustomUser.objects.create_user(
            email=email, nickname=nickname, bio=bio, password=password
        )
        if img:
            image = UserProfileImage.objects.create(user=user, img=img)
            user.profile_image = image
            user.save()

        # TODO: Celery 비동기 처리
        transaction.on_commit(lambda: send_email_verification.delay(user.id))

        return user

    @classmethod
    def verified_email_activation(cls, uidb64: str, token: str) -> CustomUser:
        """
        인증 메일을 통해 유저의 active 속성을 변경합니다.

        param
        ------
        uibd64
        token
        """
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and accounts_verify_token.check_token(
            user=user, token=token
        ):
            user.is_active = True
            user.save()

        return user

    @classmethod
    def save_like_keyword(cls, user_id: int, keyword: str):
        """
        유저가 관심있는 키워드를 저장합니다.
        """
        like_keyword, _ = UserLikeKeyWord.objects.get_or_create(
            user_id=user_id, keyword=keyword
        )
        return like_keyword
