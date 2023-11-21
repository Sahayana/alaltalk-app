from celery import shared_task
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from alaltalk.enviorment import get_current_domain
from apps.account.constants import EMAIL_VERIFY_TEMPLATE, EMAIL_VERIFY_TITLE
from apps.account.models import CustomUser
from apps.account.utils import accounts_verify_token


@shared_task
def send_email_verification(user_id: int):
    """
    새로 생성한 유저에게 사용자 인증 이메일을 전송합니다.
    """
    user = CustomUser.objects.get(id=user_id)
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
    return email_message.send()


@shared_task
def send_temporary_password(email: str, temp_pw: str):
    return send_mail(
        "[alaltalk] 임시 비밀번호 메일입니다.",
        f"회원님의 임시 비밀번호는 {temp_pw} 입니다.\n로그인 후 비밀번호를 꼭 변경해주세요.",
        "sahayana@naver.com",
        [email],
        fail_silently=False,
    )
