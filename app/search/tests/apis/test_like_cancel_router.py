from accounts.services.accounts_service import create_single_user
from django.test import RequestFactory, TestCase
from search.models import Book, News, Shopping, Youtube


class LikeCancelTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.email = "test@test.com"
        self.nickname = "test"
        self.password = "qwer1234"
        self.bio = "this is bio"
        self.user = create_single_user(
            email=self.email,
            nickname=self.nickname,
            password=self.password,
            bio=self.bio,
        )

    # 유튜브 좋아요 취소 테스트
    def test_like_cancel_youtube(self):
        # Given

        # 유저 로그인
        self.client.login(email=self.email, password=self.password)
        # request 요청 생성
        request = self.factory.get("/api/like_cancel/youtube")
        request.user = self.user

        # 유튜브 모델 생성
        test_youtube_link = "link"
        test_youtube_view = "view"
        test_youtube_title = "title"
        Youtube.objects.create(
            user=self.user,
            url=test_youtube_link,
            title=test_youtube_title,
            views=test_youtube_view,
        )

        # When
        # Content-type은 JS 에서 json이라고 보내지 않았다면 적지 않기
        response = self.client.post(
            "/api/like_cancel/youtube",
            data={
                "url": test_youtube_link,
                "title": test_youtube_title,
                "views": test_youtube_view,
            },
        )

        # Then
        self.assertEqual(201, response.status_code)
        self.assertEqual("success", response.json()["result"])

    # 유튜브 좋아요 취소 테스트 : 유저가 없을 경우
    def test_like_cancel_youtube_user_does_not_exist(self):
        # Given
        # 유저 로그인
        # request 요청 생성
        request = self.factory.get("/api/like_cancel/youtube")

        # 유튜브 모델 생성
        test_youtube_link = "link"
        test_youtube_view = "view"
        test_youtube_title = "title"
        Youtube.objects.create(
            user=self.user,
            url=test_youtube_link,
            title=test_youtube_title,
            views=test_youtube_view,
        )

        # When
        # Content-type은 JS 에서 json이라고 보내지 않았다면 적지 않기
        response = self.client.post(
            "/api/like_cancel/youtube",
            data={
                "url": test_youtube_link,
                "title": test_youtube_title,
                "views": test_youtube_view,
            },
        )

        # Then
        self.assertIsNotNone(request)
        self.assertEqual(404, response.status_code)
        self.assertEqual("User does not Exist", response.json()["detail"])

    # 유튜브 좋아요 취소 테스트 : 해당 URL이 없을 경우
    def test_like_cancel_youtube_youtube_does_not_exist(self):
        # Given
        # 유저 로그인
        # request 요청 생성
        self.client.login(email=self.email, password=self.password)
        request = self.factory.get("/api/like_cancel/youtube")
        request.user = self.user

        # JS에서 받은 값
        test_youtube_link = "link"
        test_youtube_view = "view"
        test_youtube_title = "title"

        # When
        # Content-type은 JS 에서 json이라고 보내지 않았다면 적지 않기
        response = self.client.post(
            "/api/like_cancel/youtube",
            data={
                "url": test_youtube_link,
                "title": test_youtube_title,
                "views": test_youtube_view,
            },
        )

        # Then
        self.assertEqual(404, response.status_code)
        self.assertEqual("Youtube does not Exist", response.json()["detail"])

    # 뉴스 좋아요 취소 테스트
    def test_like_cancel_news(self):
        # Given

        # 유저 로그인
        self.client.login(email=self.email, password=self.password)
        # request 요청 생성
        request = self.factory.get("/api/like_cancel/news")
        request.user = self.user

        # 뉴스 모델 생성
        title = "title"
        date = "date"
        link = "link"
        company = "company"
        content = "content"
        thumbnail = "thumbnail"
        News.objects.create(
            user=self.user,
            title=title,
            date=date,
            company=company,
            content=content,
            link=link,
            thumbnail=thumbnail,
        )

        # When
        # Content-type은 JS 에서 json이라고 보내지 않았다면 적지 않기
        response = self.client.post(
            "/api/like_cancel/news",
            data={
                "title": title,
                "date": date,
                "company": company,
                "content": content,
                "link": link,
                "thumbnail": thumbnail,
            },
        )

        # Then
        self.assertEqual(201, response.status_code)
        self.assertEqual("success", response.json()["result"])

    # 뉴스 좋아요 취소 테스트 : 유저가 없을 경우
    def test_like_cancel_news_user_does_not_exist(self):
        # Given
        # 유저 로그인
        # request 요청 생성
        request = self.factory.get("/api/like_cancel/news")

        # 뉴스 모델 생성
        title = "title"
        date = "date"
        link = "link"
        company = "company"
        content = "content"
        thumbnail = "thumbnail"
        News.objects.create(
            user=self.user,
            title=title,
            date=date,
            company=company,
            content=content,
            link=link,
            thumbnail=thumbnail,
        )

        # When
        # Content-type은 JS 에서 json이라고 보내지 않았다면 적지 않기
        response = self.client.post(
            "/api/like_cancel/news",
            data={
                "title": title,
                "date": date,
                "company": company,
                "content": content,
                "link": link,
                "thumbnail": thumbnail,
            },
        )

        # Then
        self.assertIsNotNone(request)
        self.assertEqual(404, response.status_code)
        self.assertEqual("User does not Exist", response.json()["detail"])

    # 뉴스 좋아요 취소 테스트 : 해당 URL이 없을 경우
    def test_like_cancel_news_news_does_not_exist(self):
        # Given
        # 유저 로그인
        # request 요청 생성
        self.client.login(email=self.email, password=self.password)
        request = self.factory.get("/api/like_cancel/news")
        request.user = self.user

        # JS에서 받은 값
        title = "title"
        date = "date"
        link = "link"
        company = "company"
        content = "content"
        thumbnail = "thumbnail"

        # When
        # Content-type은 JS 에서 json이라고 보내지 않았다면 적지 않기
        response = self.client.post(
            "/api/like_cancel/news",
            data={
                "title": title,
                "date": date,
                "company": company,
                "content": content,
                "link": link,
                "thumbnail": thumbnail,
            },
        )

        # Then
        self.assertEqual(404, response.status_code)
        self.assertEqual("News does not Exist", response.json()["detail"])

    # 책 좋아요 취소 테스트
    def test_like_cancel_book(self):
        # Given

        # 유저 로그인
        self.client.login(email=self.email, password=self.password)
        # request 요청 생성
        request = self.factory.get("/api/like_cancel/book")
        request.user = self.user

        # 책 모델 생성
        title = "title"
        price = "price"
        link = "link"
        company = "company"
        author = "author"
        thumbnail = "thumbnail"
        series = "series"

        Book.objects.create(
            user=self.user,
            title=title,
            price=price,
            company=company,
            author=author,
            link=link,
            thumbnail=thumbnail,
            series=series,
        )

        # When
        # Content-type은 JS 에서 json이라고 보내지 않았다면 적지 않기
        response = self.client.post(
            "/api/like_cancel/book",
            data={
                "title": title,
                "price": price,
                "company": company,
                "author": author,
                "link": link,
                "thumbnail": thumbnail,
                "series": series,
            },
        )

        # Then
        self.assertEqual(201, response.status_code)
        self.assertEqual("success", response.json()["result"])

    # 책 좋아요 취소 테스트 : 유저가 없을 경우
    def test_like_cancel_book_user_does_not_exist(self):
        # Given
        # 유저 로그인
        # request 요청 생성
        request = self.factory.get("/api/like_cancel/book")

        # 책 모델 생성
        title = "title"
        price = "price"
        link = "link"
        company = "company"
        author = "author"
        thumbnail = "thumbnail"
        series = "series"

        Book.objects.create(
            user=self.user,
            title=title,
            price=price,
            company=company,
            author=author,
            link=link,
            thumbnail=thumbnail,
            series=series,
        )

        # When
        # Content-type은 JS 에서 json이라고 보내지 않았다면 적지 않기
        response = self.client.post(
            "/api/like_cancel/book",
            data={
                "title": title,
                "price": price,
                "company": company,
                "author": author,
                "link": link,
                "thumbnail": thumbnail,
                "series": series,
            },
        )

        # Then
        self.assertIsNotNone(request)
        self.assertEqual(404, response.status_code)
        self.assertEqual("User does not exist", response.json()["detail"])

    # 책 좋아요 취소 테스트 : 해당 URL이 없을 경우
    def test_like_cancel_book_book_does_not_exist(self):
        # Given
        # 유저 로그인
        # request 요청 생성
        self.client.login(email=self.email, password=self.password)
        request = self.factory.get("/api/like_cancel/book")
        request.user = self.user

        # JS에서 받은 값
        title = "title"
        price = "price"
        link = "link"
        company = "company"
        author = "author"
        thumbnail = "thumbnail"
        series = "series"

        # When
        # Content-type은 JS 에서 json이라고 보내지 않았다면 적지 않기
        response = self.client.post(
            "/api/like_cancel/book",
            data={
                "title": title,
                "price": price,
                "company": company,
                "author": author,
                "link": link,
                "thumbnail": thumbnail,
                "series": series,
            },
        )

        # Then
        self.assertEqual(404, response.status_code)
        self.assertEqual("Book does not exist", response.json()["detail"])

    # 쇼핑 좋아요 취소 테스트
    def test_like_cancel_shopping(self):
        # Given

        # 유저 로그인
        self.client.login(email=self.email, password=self.password)
        # request 요청 생성
        request = self.factory.get("/api/like_cancel/shopping")
        request.user = self.user

        # 쇼핑 모델 생성
        title = "title"
        price = "price"
        link = "link"
        thumbnail = "thumbnail"

        Shopping.objects.create(
            user=self.user,
            title=title,
            price=price,
            link=link,
            thumbnail=thumbnail,
        )

        # When
        # Content-type은 JS 에서 json이라고 보내지 않았다면 적지 않기
        response = self.client.post(
            "/api/like_cancel/shopping",
            data={
                "title": title,
                "price": price,
                "link": link,
                "thumbnail": thumbnail,
            },
        )

        # Then
        self.assertEqual(201, response.status_code)
        self.assertEqual("success", response.json()["result"])

    # 쇼핑 좋아요 취소 테스트 : 유저가 없을 경우
    def test_like_cancel_shopping_user_does_not_exist(self):
        # Given
        # 유저 로그인
        # request 요청 생성
        request = self.factory.get("/api/like_cancel/shopping")

        # 쇼핑 모델 생성
        title = "title"
        price = "price"
        link = "link"
        thumbnail = "thumbnail"

        Shopping.objects.create(
            user=self.user,
            title=title,
            price=price,
            link=link,
            thumbnail=thumbnail,
        )

        # When
        # Content-type은 JS 에서 json이라고 보내지 않았다면 적지 않기
        response = self.client.post(
            "/api/like_cancel/shopping",
            data={
                "title": title,
                "price": price,
                "link": link,
                "thumbnail": thumbnail,
            },
        )

        # Then
        self.assertIsNotNone(request)
        self.assertEqual(404, response.status_code)
        self.assertEqual("User does not Exist", response.json()["detail"])

    # 책 좋아요 취소 테스트 : 해당 URL이 없을 경우
    def test_like_cancel_shopping_shopping_does_not_exist(self):
        # Given
        # 유저 로그인
        # request 요청 생성
        self.client.login(email=self.email, password=self.password)
        request = self.factory.get("/api/like_cancel/shopping")
        request.user = self.user

        # JS에서 받은 값
        title = "title"
        price = "price"
        link = "link"
        thumbnail = "thumbnail"

        # When
        # Content-type은 JS 에서 json이라고 보내지 않았다면 적지 않기
        response = self.client.post(
            "/api/like_cancel/shopping",
            data={
                "title": title,
                "price": price,
                "link": link,
                "thumbnail": thumbnail,
            },
        )

        # Then
        self.assertEqual(404, response.status_code)
        self.assertEqual("Shopping does not Exist", response.json()["detail"])
