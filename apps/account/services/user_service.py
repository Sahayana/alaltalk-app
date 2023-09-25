from django.core.mail import EmailMessage
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from alaltalk.enviorment import get_current_domain
from apps.accounts.constants import EMAIL_VERIFY_TEMPLATE, EMAIL_VERIFY_TITLE
from apps.accounts.models import CustomUser, UserProfileImage
from apps.accounts.utils import accounts_verify_token


class UserService:
    def _send_email_verification(self, user: CustomUser) -> None:

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

    @transaction.atomic()
    def create_single_user(
        self, email: str, nickname: str, password: str, img: None
    ) -> CustomUser:

        user = CustomUser.objects.create_user(
            email=email, nickname=nickname, password=password
        )
        if img:
            UserProfileImage.objects.create(user=user, img=img)

        # TODO: Celery 비동기 처리
        self._send_email_verification(user=user)

        return user

    def verified_email_activation(self, uidb64: str, token: str) -> None:

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
