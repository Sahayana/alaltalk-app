from rest_framework_simplejwt.tokens import RefreshToken

from apps.account.models import CustomUser


def authorization_header(user: CustomUser):
    """
    header 인증
    """
    refresh = RefreshToken.for_user(user=user)
    return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}
