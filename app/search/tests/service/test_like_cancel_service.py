from accounts.models import CustomUser
from django.test import TestCase
from search.models import Book, News, Shopping, Youtube
from search.service.like_cancel_service import (
    like_cancel_book,
    like_cancel_news,
    like_cancel_shopping,
    like_cancel_youtube,
)


class TestLikeCancelService(TestCase):
    def test_like_cancel_youtube(self) -> None:
        # Given
        email = "test@test.com"
        nickname = "testuser1"
        password = "testuser1"
        bio = "testuser1"
        user = CustomUser.objects.create_user(
            email=email, nickname=nickname, password=password, bio=bio
        )

        youtube_url = "test_url"
        title = "test_youtube_title"
        views = "test_youtube_view"
        Youtube.objects.create(user=user, url=youtube_url, title=title, views=views)

        # When
        like_cancel_youtube(user.id, youtube_url)
        exist_youtube = Youtube.objects.filter(user=user, url=youtube_url)

        # Then
        self.assertFalse(exist_youtube)

    def test_like_cancel_news(self) -> None:
        # Given
        email = "test@test.com"
        nickname = "testuser1"
        password = "testuser1"
        bio = "testuser1"
        user = CustomUser.objects.create_user(
            email=email, nickname=nickname, password=password, bio=bio
        )

        title = "test_news_title"
        date = "test_news_date"
        company = "test_news_company"
        content = "test_news_content"
        thumbnail_url = "test_news_thumbnail_url"
        link_url = "test_news_link_url"
        News.objects.create(
            user=user,
            title=title,
            date=date,
            company=company,
            content=content,
            thumbnail=thumbnail_url,
            link=link_url,
        )

        # When
        like_cancel_news(user.id, link_url)
        exist_news = News.objects.filter(user=user, link=link_url)

        # Then
        self.assertFalse(exist_news)

    def test_like_cancel_book(self) -> None:
        # Given
        email = "test@test.com"
        nickname = "testuser1"
        password = "testuser1"
        bio = "testuser1"
        user = CustomUser.objects.create_user(
            email=email, nickname=nickname, password=password, bio=bio
        )

        title = "test_book_title"
        price = "test_book_price"
        author = "test_book_author"
        company = "test_book_company"
        thumbnail = "test_book_thumbnail"
        link = "test_book_link"
        series = "test_book_series"
        Book.objects.create(
            user=user,
            link=link,
            title=title,
            price=price,
            author=author,
            company=company,
            thumbnail=thumbnail,
            series=series,
        )

        # When
        like_cancel_book(user.id, link)
        exist_book = Book.objects.filter(user=user, link=link)

        # Then
        self.assertFalse(exist_book)

    def test_like_cancel_shopping(self) -> None:
        # Given
        email = "test@test.com"
        nickname = "testuser1"
        password = "testuser1"
        bio = "testuser1"
        user = CustomUser.objects.create_user(
            email=email, nickname=nickname, password=password, bio=bio
        )

        title = "test_shopping_title"
        price = "test_shopping_price"
        thumbnail_url = "test_shopping_thumbnail_url"
        link_url = "test_shopping_link_url"
        Shopping.objects.create(
            user=user, title=title, price=price, thumbnail=thumbnail_url, link=link_url
        )

        # When
        like_cancel_shopping(user.id, link_url)
        exist_shopping = Shopping.objects.filter(user=user, link=link_url)

        # Then
        self.assertFalse(exist_shopping)
