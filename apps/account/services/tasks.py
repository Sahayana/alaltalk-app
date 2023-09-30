from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from alaltalk.enviorment import get_current_domain
from apps.account.constants import EMAIL_VERIFY_TEMPLATE, EMAIL_VERIFY_TITLE
from apps.account.models import CustomUser
from apps.account.utils import accounts_verify_token


@shared_task
def send_email_verification(user: CustomUser) -> None:
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
