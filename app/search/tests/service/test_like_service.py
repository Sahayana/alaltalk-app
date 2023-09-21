from accounts.models import CustomUser
from django.test import TestCase
from search.service.like_service import (
    do_like_book_service,
    do_like_news_service,
    do_like_shopping_service,
    do_like_youtube_service,
)


class TestLikeService(TestCase):
    def test_do_like_youtube_service(self) -> None:
        # Given
        email = "test@test.com"
        nickname = "testuser1"
        password = "testuser1"
        bio = "testuser1"
        user = CustomUser.objects.create_user(
            email=email, nickname=nickname, password=password, bio=bio
        )

        user_id = user.id
        youtube_url = "test_url"
        title = "test_youtube_title"
        views = "test_youtube_view"

        # When
        like_youtube = do_like_youtube_service(user_id, youtube_url, title, views)

        # Then
        self.assertEqual("success", like_youtube)

    def test_do_like_shopping_service(self) -> None:
        # Given
        email = "test@test.com"
        nickname = "testuser1"
        password = "testuser1"
        bio = "testuser1"
        user = CustomUser.objects.create_user(
            email=email, nickname=nickname, password=password, bio=bio
        )
        user_id = user.id
        title = "test_shopping_title"
        price = "test_shopping_price"
        thumbnail_url = "test_shopping_thumbnail_url"
        link_url = "test_shopping_link_url"

        # When
        like_shopping = do_like_shopping_service(
            user_id, title, price, thumbnail_url, link_url
        )

        # Then
        self.assertEqual("success", like_shopping)

    def test_do_like_book_service(self) -> None:
        # Given
        email = "test@test.com"
        nickname = "testuser1"
        password = "testuser1"
        bio = "testuser1"
        user = CustomUser.objects.create_user(
            email=email, nickname=nickname, password=password, bio=bio
        )

        user_id = user.id
        title = "test_book_title"
        price = "test_book_price"
        author = "test_book_author"
        company = "test_book_company"
        thumbnail = "test_book_thumbnail"
        link = "test_book_link"
        series = "test_book_series"

        # When
        like_book = do_like_book_service(
            user_id, title, price, author, company, thumbnail, link, series
        )

        # Then
        self.assertEqual("success", like_book)

    def test_do_like_news_service(self) -> None:
        # Given
        email = "test@test.com"
        nickname = "testuser1"
        password = "testuser1"
        bio = "testuser1"
        user = CustomUser.objects.create_user(
            email=email, nickname=nickname, password=password, bio=bio
        )

        user_id = user.id
        title = "test_news_title"
        date = "test_news_date"
        company = "test_news_company"
        content = "test_news_content"
        thumbnail_url = "test_news_thumbnail_url"
        link_url = "test_news_link_url"

        # When
        like_news = do_like_news_service(
            user_id, title, date, company, content, thumbnail_url, link_url
        )

        # Then
        self.assertEqual("success", like_news)
