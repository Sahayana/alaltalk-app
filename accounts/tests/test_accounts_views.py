import email
import re
from urllib import response
from attr import resolve_types
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from accounts.models import CustomUser, FriendRequest
from accounts.services.accounts_service import create_single_user, send_friend_request
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime

class TestAccountsViews(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.email = 'test@test.com'
        self.nickname = 'test'
        self.password = 'test'
        self.bio = 'dj@coplsd@'
        self.user = create_single_user(email=self.email, nickname=self.nickname, password=self.password, bio=self.bio)
        self.user2 = create_single_user(email='friend@friend.com', nickname='friend', password=self.password, bio='test2')


    def test_get_sign_up_page(self) -> None:

        # When
        response = self.client.get(reverse('accounts:signup'))
        
        # Then
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name="accounts/signup.html")
        
    def test_post_sign_up_page(self) -> None:        
        
        # When
        response = self.client.post(
            reverse("accounts:signup"),
            data = {
            "email":"test2@test.com",
            "nickname":"test2",
            "password":"test2",
            "bio":"test2",
            },            
        )

        users = get_user_model().objects.all()

        # Then
        self.assertEqual(201, response.status_code)
        self.assertIsNotNone(response.json()["result"])        
        self.assertEqual(3, users.count())
        self.assertIsNotNone(users[1].img)
        
    def test_duplicated_check(self) -> None:

        # When
        response = self.client.get(
            reverse("accounts:duplicated_check") + f'?email={self.user.email}'
        )

        # Then
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json()["duplicated"])
        self.assertTrue(response.json()["duplicated"])

    def test_get_login_page(self) -> None:

        # When
        response = self.client.get(
            reverse("accounts:login")
        )
        
        # Given
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name="accounts/login.html")

    def test_post_login_page_with_registered_user(self) -> None:
        
        # Given
        user = self.user
        data = {
            'email':user.email,
            'password':self.password
        }       

        # When
        response = self.client.post(
            reverse('accounts:login'),
            data=data
        )
        
        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual("ok", response.json()["msg"])
       
    def test_post_login_page_with_unregistered_user(self) -> None:
        
        # Given
        unvalid_email = 'notuser@notuser.com'
        unvalid_password = 'notuser'
        data = {
            'email':unvalid_email,
            'password':unvalid_password
        }

        # When
        response = self.client.post(
            reverse("accounts:login"),
            data=data
        )
        
        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual("error", response.json()["msg"])

    def test_redirect_when_logged_in_user_get_login_page(self) -> None:
        
        # Given        
        login_user = self.client.login(email=self.email, password=self.password)

        # When
        response = self.client.get(
            reverse("accounts:login")
        )

        # Then
        self.assertTrue(login_user)
        self.assertRedirects(
            response=response,
            expected_url=reverse("accounts:mypage")
        )
    
    def test_logout_when_not_logged_in(self) -> None:

        # When
        response = self.client.get(
            reverse("accounts:logout")
        )

        # Then
        self.assertRedirects(
            response=response,
            expected_url='/accounts/login/?next=/accounts/logout/'
        )

    def test_logout(self) -> None:
        
        # Given
        login_user = self.client.login(email=self.email, password=self.password)

        # When
        response = self.client.get(
            reverse("accounts:logout")
        )

        # Then
        self.assertTrue(login_user)
        self.assertRedirects(response, '/')

    def test_get_friend_list(self) -> None:
        
        # Given
        login_user = self.client.login(email=self.email, password=self.password)

        # When
        response = self.client.get(reverse('accounts:friend_list'))
        user = self.user

        # Then
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "accounts/user_list.html")
        self.assertTrue(login_user)
        self.assertEqual(user, response.context['user'])
        self.assertEqual(user.id, response.context['user'].id)
        self.assertEqual(0, len(response.context['friends']))
        self.assertIsInstance(response.context['user'], CustomUser)

    def test_get_mypage(self) -> None:
        
        # Given
        login_user = self.client.login(email=self.email, password=self.password)

        # When
        response = self.client.get(reverse('accounts:mypage'))
        user = self.user

        # Then
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "accounts/mypage.html")
        self.assertTrue(login_user)
        self.assertIsInstance(user, CustomUser)

    def test_post_profile_change(self) -> None:
        
        # Given
        login_user = self.client.login(email=self.email, password=self.password)
        request = self.factory.get(reverse("accounts:profile_change"))
        request.user = self.user
        data = {
            "nickname":"changed_nickname",
            "password":"changed_pw",
            "bio":"changed_bio",
        }
        
        
        # When
        response = self.client.post(
            reverse("accounts:profile_change"),
            data=data
        )

        changed_user = CustomUser.objects.get(id=request.user.id)
        
        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual("changed_nickname", changed_user.nickname)        
        self.assertEqual("changed_bio", changed_user.bio)
        self.assertEqual("ok", response.json()['msg'])
    
    def test_post_profile_image_change(self) -> None:
        
        # Given
        login_user = self.client.login(email=self.email, password=self.password)
        request = self.factory.get(reverse("accounts:profile_change"))
        request.user = self.user
        data = {
            "nickname":"changed_nickname",            
            "bio":"changed_bio",
            "img" : SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        }

        # When
        response = self.client.post(
            reverse("accounts:profile_change"),
            data=data
        )

        changed_user = CustomUser.objects.get(id=request.user.id)
        username, domain = changed_user.email.split('@')
        img_extension = 'jpg'
        img_upload_to = "profile_img/"

        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual("changed_nickname", changed_user.nickname)        
        self.assertEqual("changed_bio", changed_user.bio)
        self.assertEqual(
            changed_user.img.name,
            img_upload_to + username + domain.split('.')[0] + domain.split('.')[1] + "-" + datetime.now().strftime("%Y-%m-%d") + "." + img_extension
            )

    
    def test_get_search_friend(self) -> None:

        # Given
        login_user = self.client.login(email=self.email, password=self.password)
        request = self.factory.get(reverse("accounts:search_friend"))
        request.user = self.user
        query = 'test'

        # When
        response = self.client.get(
            reverse("accounts:search_friend") + f'?q={query}'
        )
        current_user = CustomUser.objects.filter(id=request.user.id).get()

        # Then
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json()['result'])
        self.assertEqual(1, len(response.json()['result']))
        self.assertEqual(1, response.json()['result'][0][1])
        self.assertEqual(current_user.id, response.json()['result'][0][0]['id'])

    def test_view_search_friend_returns_none(self) -> None:

        # Given
        login_user = self.client.login(email=self.email, password=self.password)
        request = self.factory.get(reverse("accounts:search_friend"))
        request.user = self.user
        invalid_query = "nobody"

        # When
        response = self.client.get(
            reverse("accounts:search_friend") + f'?q={invalid_query}'
        )        
        
        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual("none", response.json()["msg"])


    def test_send_friend_request(self) -> None:

        # Given
        login_user = self.client.login(email=self.email, password=self.password)
        request = self.factory.get(reverse("accounts:search_friend"))
        request.user = self.user
        user2 = self.user2

        # When
        response = self.client.get(
            reverse("accounts:send_request", kwargs={"receiver_id":user2.id})
        )

        friend_requests = FriendRequest.objects.all()

        # Then
        self.assertTrue(login_user)
        self.assertEqual(201, response.status_code)
        self.assertEqual("sent", response.json()['msg'])
        self.assertEqual(1, friend_requests.count())
        self.assertEqual(request.user.id, friend_requests[0].sender.id)
        self.assertEqual(user2.id, friend_requests[0].receiver.id)
    
    def test_send_friend_request_already_sent(self) -> None:

        # Given
        login_user = self.client.login(email=self.email, password=self.password)
        request = self.factory.get(reverse("accounts:search_friend"))
        request.user = self.user
        user2 = self.user2
        friend_request, created = send_friend_request(sender_id=request.user.id, recevier_id=user2.id)

        # When
        response = self.client.get(
            reverse("accounts:send_request", kwargs={"receiver_id":user2.id})
        )

        friend_requests = FriendRequest.objects.all()

        # Then
        self.assertEqual("already", response.json()["msg"])
        self.assertEqual(1, friend_requests.count())
        self.assertEqual(friend_request.id, friend_requests[0].id)

    def test_accept_friend_request(self) -> None:
        
        # Given
        login_user = self.client.login(email=self.email, password=self.password)
        request = self.factory.get(reverse("accounts:search_friend"))
        request.user = self.user
        user2 = self.user2
        friend_request, created = send_friend_request(sender_id=user2.id, recevier_id=request.user.id)


        # When
        response = self.client.get(
            reverse("accounts:accept_request", kwargs={"request_id": friend_request.id})
        )
        friend_requests = FriendRequest.objects.all()

        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, friend_requests.count())
        self.assertEqual(1, request.user.friends.all().count())
        self.assertEqual(1, user2.friends.all().count())
        self.assertEqual(user2.id, request.user.friends.all()[0].id)
        self.assertEqual(request.user.id, user2.friends.all()[0].id)

    def test_decline_friend_request(self) -> None:

        # Given
        login_user = self.client.login(email=self.email, password=self.password)
        request = self.factory.get(reverse("accounts:search_friend"))
        request.user = self.user
        user2 = self.user2
        friend_request, created = send_friend_request(sender_id=user2.id, recevier_id=request.user.id)
        
        # When
        response = self.client.get(
            reverse("accounts:decline_request", kwargs={"request_id": friend_request.id})
        )
        friend_requests = FriendRequest.objects.all()
        
        # Then
        self.assertEqual(200, response.status_code)
        self.assertNotIn(request.user, user2.friends.all())
        self.assertEqual(0, friend_requests.count())

    def test_send_temporary_password(self) -> None:

        # Given
        email = self.email

        # When
        response = self.client.get(
            reverse("accounts:temporary_password") + f'?q={email}'
        )
        pw_changed_user = CustomUser.objects.get(email=self.email)

        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual("ok", response.json()['msg'])
        self.assertFalse(pw_changed_user.check_password(self.password))

    def test_send_temporary_password_with_unvalid_email(self) -> None:

        # Given
        unvalid_email = 'unvalid@unvalid.com'

        # When
        response = self.client.get(
            reverse("accounts:temporary_password") + f'?q={unvalid_email}'
        )
        current_user = CustomUser.objects.get(email=self.email)

        # Then
        self.assertEqual("none-user", response.json()['msg'])
        self.assertTrue(current_user.check_password(self.password))
        
    def test_auth_check(self) -> None:

        # Given
        login_user = self.client.login(email=self.email, password=self.password)
        request = self.factory.get(reverse("accounts:mypage"))
        request.user = self.user
        data = {"password":self.password}

        # When
        response = self.client.post(
            reverse("accounts:auth_check"),
            data=data
        )

        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual("ok", response.json()['msg'])

    def test_auth_check_failed(self) -> None:

        # Given
        login_user = self.client.login(email=self.email, password=self.password)
        request = self.factory.get(reverse("accounts:mypage"))
        request.user = self.user
        unvalid_pw = 'unvalid_pw'
        data = {"password":unvalid_pw}

        # When
        response = self.client.post(
            reverse("accounts:auth_check"),
            data=data
        )

        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual("no", response.json()['msg'])

    
    def test_view_profile_delete(self) -> None:

        # Given
        login_user = self.client.login(email=self.email, password=self.password)
        request = self.factory.get(reverse("accounts:mypage"))
        request.user = self.user

        # When
        response = self.client.get(reverse("accounts:profile_delete"))
        
        all_users = CustomUser.objects.all()

        # Then
        self.assertEqual(200, response.status_code)
        self.assertNotIn(request.user.id, [user.id for user in all_users])
        self.assertEqual("deleted", response.json()["msg"])

    
    def test_view_remove_friend(self) -> None:

        # Given
        login_user = self.client.login(email=self.email, password=self.password)
        request = self.factory.get(reverse("accounts:mypage"))
        request.user = self.user
        request.user.friends.add(self.user2)
        self.user2.friends.add(request.user)

        # When
        response = self.client.get(
            reverse("accounts:remove_friend", kwargs={"friend_id": self.user2.id})
        )

        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, request.user.friends.count())
        self.assertEqual(0, self.user2.friends.count())
        self.assertEqual("deleted", response.json()["msg"])