from django.core.mail import EmailMessage
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from alaltalk.enviorment import get_current_domain
from apps.account.constants import EMAIL_VERIFY_TEMPLATE, EMAIL_VERIFY_TITLE
from apps.account.models import CustomUser, UserProfileImage
from apps.account.utils import accounts_verify_token


class UserService:
    @classmethod
    def _send_email_verification(self, user: CustomUser) -> None:
        """
        새로 생성한 유저에게 사용자 인증 이메일을 전송합니다.
        """

        message = render_to_string(
            template_name=EMAIL_VERIFY_TEMPLATE,
            context={
                "user": user,
                "domain": get_current_domain(),
                "uid": urlsafe_base64_encode(force_bytes(user.id)).encode().decode(),
                "token": accounts_verify_token.make_token(user),
            },
        )
        email_message = EmailMessage(EMAIL_VERIFY_TITLE, message, to=[user.email])
        email_message.send()

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
        cls._send_email_verification(user=user)

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
