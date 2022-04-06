from django.test import TestCase, RequestFactory
from accounts.services.accounts_service import create_single_user
from search.models import Youtube


class TestLikeCancelService(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.email = 'test@test.com'
        self.nickname = 'test'
        self.password = 'qwer1234'
        self.bio = 'this is bio'
        self.user = create_single_user(email=self.email, nickname=self.nickname, password=self.password, bio=self.bio)

    # 유튜브 좋아요 테스트
    def test_do_like_Youtube(self) -> None:
        # Given

        # 유저 로그인
        self.client.login(email=self.email, password=self.password)
        # request 요청 생성
        request = self.factory.get('/api/like/youtube')

        # JS 에서 전달 받을 테스트 값들
        test_youtube_link = 'link'
        test_youtube_view = 'view'
        test_youtube_title = 'title'

        # When
        # Content-type은 JS 에서 json이라고 보내지 않았다면 적지 않기
        response = self.client.post(
            f"/api/like/youtube",
            data={
                "url": test_youtube_link,
                'title': test_youtube_title,
                'views': test_youtube_view
            },
        )

        # Then
        self.assertEqual(201, response.status_code)
        self.assertEqual('success', response.json()['result'])

    # 유튜브 이미 등록된
    def test_already_like_youtube(self) -> None:
        # Given
        # 유저 로그인
        self.client.login(email=self.email, password=self.password)
        # request 요청 생성
        request = self.factory.get('/api/like/youtube')
        # request.user = self.user

        # JS 에서 전달 받을 테스트 값들
        test_youtube_link = 'link'
        test_youtube_view = 'view'
        test_youtube_title = 'title'
        Youtube.objects.create(user=self.user, url=test_youtube_link, views=test_youtube_view, title=test_youtube_title)

        # When
        # Content-type은 JS 에서 json이라고 보내지 않았다면 적지 않기
        response = self.client.post(
            f"/api/like/youtube",
            data={
                "url": test_youtube_link,
                'title': test_youtube_title,
                'views': test_youtube_view
            },
        )

        # Then
        self.assertEqual(201, response.status_code)
        self.assertEqual('AlreadyExist', response.json()['result'])

    def test_like_youtube_user_does_not_exist(self) -> None:
        # Given
        request = self.factory.get('api/like/youtube')
        test_youtube_link = 'link'
        test_youtube_view = 'view'
        test_youtube_title = 'title'

        # When
        response = self.client.post(
            f"/api/like/youtube",
            data={
                "url": test_youtube_link,
                'title': test_youtube_title,
                'views': test_youtube_view
            },
        )

        # Then
        self.assertEqual(404, response.status_code)
        self.assertEqual('User is not Exist', response.json()['detail'])

    # 뉴스 찜 테스트
    def test_like_news(self) -> None:
        # Given
        self.client.login(email=self.email, password=self.password)
        request = self.factory.get('/api/like/news')
        request.user = self.user
        title = 'news_title'
        date = 'news_data'
        link = 'news_link'
        company = 'news_company'
        content = 'news_content'
        thumbnail = 'news_thumbnail'

        # When
        response = self.client.post(
            f"/api/like/news",
            data={
                "title": title,
                'date': date,
                'link': link,
                'company': company,
                'content': content,
                'thumbnail': thumbnail,
            },
        )

        # Then
        self.assertEqual(201, response.status_code)

    def test_like_book(self) -> None:
        # Given
        self.client.login(email=self.email, password=self.password)
        request = self.factory.get('/api/like/book')
        request.user = self.user
        title = 'book_title'
        date = 'book_data'
        link = 'book_link'
        company = 'book_company'
        content = 'book_content'
        thumbnail = 'book_thumbnail'
        series= 'book_series'

        # When
        response = self.client.post(
            f"/api/like/book",
            data={
                "title": title,
                'price': date,
                'link': link,
                'company': company,
                'author': content,
                'thumbnail': thumbnail,
                'series': series,
            },
        )

        # Then
        self.assertEqual(201, response.status_code)

    def test_like_shopping(self) -> None:
        # Given
        self.client.login(email=self.email, password=self.password)
        request = self.factory.get('/api/like/shopping')
        request.user = self.user
        title = 'shopping_title'
        link = 'shopping_link'
        price = 'shopping_price'
        thumbnail = 'shopping_thumbnail'

        # When
        response = self.client.post(
            f"/api/like/shopping",
            data={
                "title": title,
                'link': link,
                'price': price,
                'thumbnail': thumbnail,
            },
        )

        # Then
        self.assertEqual(201, response.status_code)
