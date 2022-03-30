
from search.models import Shopping, Book, News
from accounts.models import CustomUser
from search.models import Youtube


def like_cancel_youtube(user_id: int, youtube_url: str) -> None:
    user = CustomUser.objects.get(pk=user_id)
    Youtube.objects.get(user=user, url=youtube_url).delete()


def like_cancel_news(user_id: int, news_url: str) -> None:
    user = CustomUser.objects.get(pk=user_id)
    News.objects.get(user=user, link=news_url).delete()


def like_cancel_book(user_id: int, book_url: str) -> None:
    user = CustomUser.objects.get(pk=user_id)
    Book.objects.get(user=user, link=book_url).delete()


def like_cancel_shopping(user_id: int, shopping_url: str) -> None:
    user = CustomUser.objects.get(pk=user_id)
    Shopping.objects.get(user=user, link=shopping_url).delete()

