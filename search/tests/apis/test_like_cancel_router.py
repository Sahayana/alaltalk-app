from django.test import TestCase, RequestFactory
from accounts.models import CustomUser


class TestLikeCancelService(TestCase):
    def setup(self):
        self.factory = RequestFactory()

        self.user = CustomUser.objects.create_user(email="test@test.com", nickname="testuser1", password="qwer1234", bio="test")

    def test_do_like_Youtube(self) -> None:
        # Given
        login_user = self.client.login(email="test@test.com", password="qwer1234")
        test_youtube_link = 'link'
        test_youtube_view = 'view'
        test_youtube_title = 'title'

        # When
        response = self.client.post(
            f"/api/like/youtube/",
            data={
                'url': test_youtube_link,
                'title': test_youtube_title,
                'views': test_youtube_view
            },
            content_type="application/json",
        )

        # Then
        print(response)
        self.assertEqual(201, response.status_code)