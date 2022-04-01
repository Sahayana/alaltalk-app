from django.test import TestCase
from django.urls import reverse


class TestAccountsViews(TestCase):

    def test_get_sign_up_page(self) -> None:

        # When
        response = self.client.get(reverse('accounts:signup'))
        
        # Then
        self.assertEqual(200, response.status_code)
        