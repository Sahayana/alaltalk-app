from search.models import Youtube
from accounts.models import CustomUser


def like_cancel_youtube(user_id: int, youtube_url: str) -> None:
    user = CustomUser.objects.get(pk=user_id)
    Youtube.objects.get(user=user, url=youtube_url).delete()
