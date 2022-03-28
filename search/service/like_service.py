from accounts.models import CustomUser
from ..models import Youtube, Book, Shopping, News


def do_like_youtube_service(user_id: int, youtube_url: str) -> str:
    user = CustomUser.objects.get(pk=user_id)
    youtube_check = Youtube.objects.filter(user=user, url=youtube_url).exists()
    if not youtube_check:
        Youtube.objects.create(user=user, url=youtube_url)
        return 'success'
    else:
        return 'AlreadyExist'


def do_like_shopping_service(user_id: int, title: str, price: str, thumbnail_url: str, link_url: str) -> str:
    user = CustomUser.objects.get(pk=user_id)
    shopping_check = Shopping.objects.filter(user=user, link=link_url).exists()
    if not shopping_check:
        Shopping.objects.create(user=user, title=title, price=price, thumbnail=thumbnail_url, link=link_url)
        return 'success'
    else:
        return 'AlreadyExist'

