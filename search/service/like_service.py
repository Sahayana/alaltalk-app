from accounts.models import CustomUser

from ..models import Book, News, Shopping, Youtube


def do_like_youtube_service(user_id: int, youtube_url: str, title: str, views: str) -> str:
    user = CustomUser.objects.get(pk=user_id)
    youtube_check = Youtube.objects.filter(user=user, url=youtube_url).exists()
    if not youtube_check:
        Youtube.objects.create(user=user, url=youtube_url, title=title, views=views)
        return "success"
    else:
        return "AlreadyExist"


def do_like_shopping_service(user_id: int, title: str, price: str, thumbnail_url: str, link_url: str) -> str:
    user = CustomUser.objects.get(pk=user_id)
    shopping_check = Shopping.objects.filter(user=user, link=link_url).exists()
    if not shopping_check:
        Shopping.objects.create(user=user, title=title, price=price, thumbnail=thumbnail_url, link=link_url)
        return "success"
    else:

        return "AlreadyExist"


def do_like_book_service(user_id: int, title: str, price: str, author: str, company: str, thumbnail: str, link: str, series: str) -> str:
    user = CustomUser.objects.get(pk=user_id)
    book_check = Book.objects.filter(user=user, link=link).exists()
    if not book_check:
        Book.objects.create(user=user, link=link, title=title, price=price, author=author, company=company, thumbnail=thumbnail, series=series)
        return "success"
    else:
        return "AlreadyExist"


def do_like_news_service(user_id: int, title: str, date: str, company: str, content: str, thumbnail_url: str, link_url: str) -> str:
    user = CustomUser.objects.get(pk=user_id)
    news_check = News.objects.filter(user=user, link=link_url).exists()
    if not news_check:
        News.objects.create(user=user, title=title, date=date, company=company, content=content, thumbnail=thumbnail_url, link=link_url)
        return "success"
    else:
        return "AlreadyExist"
