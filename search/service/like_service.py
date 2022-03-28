from accounts.models import CustomUser
from ..apis.v1.schemas import YoutubeLikeRequest, YoutubeLikeResponse
from ..models import Youtube, Book, Shopping, News


def do_like_youtube_service(user_id: int, youtube_content: YoutubeLikeRequest) -> str:
    user = CustomUser.objects.get(pk=user_id)
    youtube_check = Youtube.objects.filter(user=user, url=youtube_content.url).exists()
    if not youtube_check:
        Youtube.objects.create(user=user, url=youtube_content.url)
        return 'success'
    else:
        return 'AlreadyExist'

