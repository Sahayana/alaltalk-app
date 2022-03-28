from search.models import Youtube, Shopping, Book
from accounts.models import CustomUser


def like_cancel_youtube(user_id: int, youtube_url: str) -> None:
    user = CustomUser.objects.get(pk=user_id)
    Youtube.objects.get(user=user, url=youtube_url).delete()


def like_cancel_shopping(user_id: int, shopping_link: str) -> None:
    user = CustomUser.objects.get(pk=user_id)
    Shopping.objects.get(user=user, link=shopping_link).delete()


def like_cancel_book(user_id: int, book_link: str) -> None:
    user = CustomUser.objects.get(pk=user_id)
    Book.objects.get(user=user, link=book_link).delete()
