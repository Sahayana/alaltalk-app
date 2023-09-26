from apps.account.models import CustomUser


class UserSelector:
    """
    유저 모델의 조회 쿼리와 관련된 서비스를 정의합니다.
    """

    def check_email_duplication(self, email: str) -> bool:
        return CustomUser.objects.filter(email__iexact=email).exists()

    def get_user_by_id(self, user_id: int) -> CustomUser:
        try:
            user = CustomUser.objects.filter(id=user_id).get()
        except CustomUser.DoesNotExist:
            return None
        return user
