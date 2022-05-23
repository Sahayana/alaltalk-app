from django.contrib.auth.hashers import check_password
from django.core import mail
from django.test import TestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.models import CustomUser, FriendRequest
from accounts.services.accounts_service import (
    accept_friend_request,
    accounts_delete_friend,
    accounts_profile_delete,
    check_authentication,
    check_email_duplication,
    create_single_user,
    decline_friend_request,
    get_friend_list,
    send_email_verification,
    send_friend_request,
    verified_email_activation,
    accounts_token_authenticated,
    accounts_search_friends
)
from accounts.utils import accounts_verify_token
import jwt
from alaltalk.settings import SECRET_KEY





class AccountsTest(TestCase):
    def test_create_a_single_user(self) -> None:
        # Given
        email = "test@test.com"
        nickname = "testuser1"
        password = "testuser1"
        bio = "testuser1"

        # When
        user = create_single_user(email=email, nickname=nickname, password=password, bio=bio)

        # Then
        self.assertEqual(1, user.id)
        self.assertEqual("testuser1", user.bio)

    def test_check_if_an_email_is_already_exists(self) -> None:
        # Given
        email = "test@test.com"
        nickname = "testuser1"
        password = "testuser1"
        user = create_single_user(email=email, nickname=nickname, password=password)

        # When
        duplicated = check_email_duplication(email=email)

        # Then
        self.assertTrue(duplicated)

    # def test_if_an_user_can_change_profile(self) -> None:
    #     # Given
    #     user = create_single_user(email="test@test.com", nickname="testuser1", password="testuser1", bio="testuser1")

    #     nickname = 'testuser1_changed'
    #     bio = 'testuser1_changed'
    #     password = 'testuser1_ch'

    #     # When
    #     user_modified = change_user_profile(user=user, nickname=nickname, bio=bio, password=password)

    #     # Then
    #     self.assertEqual('testuser1_changed', user_modified.nickname)
    #     self.assertEqual(user.id, user_modified.id)
    #     self.assertFalse(check_password(user.password, user_modified.password))
    #     self.assertIsNotNone(user_modified.img.url)

    def test_get_friend_list(self) -> None:

        # Given
        user = create_single_user(email="test@test.com", nickname="testuser1", password="testuser1", bio="testuser1")
        friend = create_single_user(email="test2@test.com", nickname="testuser2", password="testuser2", bio="testuser2")
        user.friends.add(friend)
        friend.friends.add(friend)

        # When
        friends = get_friend_list(user_id=user.id)

        # Then
        self.assertIsNotNone(user.friends.all())
        self.assertEqual(1, len(friends))
        self.assertEqual(1, len(friend.friends.all()))
        self.assertEqual(friend.id, user.friends.all()[0].id)

    def test_send_friend_request(self) -> None:

        # Given
        sender = create_single_user(email="test@test.com", nickname="testuser1", password="testuser1", bio="testuser1")
        receiver = create_single_user(email="test2@test.com", nickname="testuser2", password="testuser2", bio="testuser2")

        # When
        friend_requests, is_created = send_friend_request(sender_id=sender.id, recevier_id=receiver.id)

        # Then
        self.assertIsNotNone(friend_requests)
        self.assertTrue(is_created)

    def test_send_duplicated_friend_request(self) -> None:

        # Given
        sender = create_single_user(email="test@test.com", nickname="testuser1", password="testuser1", bio="testuser1")
        receiver = create_single_user(email="test2@test.com", nickname="testuser2", password="testuser2", bio="testuser2")
        friend_request, _ = send_friend_request(sender_id=sender.id, recevier_id=receiver.id)

        # When
        friend_request2, is_created = send_friend_request(sender_id=sender.id, recevier_id=receiver.id)

        # Then
        self.assertIsNotNone(friend_request)
        self.assertEqual(friend_request, friend_request2)
        self.assertFalse(is_created)

    def test_accept_friend_request(self) -> None:

        # Given
        sender = create_single_user(email="test@test.com", nickname="testuser1", password="testuser1", bio="testuser1")
        receiver = create_single_user(email="test2@test.com", nickname="testuser2", password="testuser2", bio="testuser2")
        friend_request, is_created = send_friend_request(sender_id=sender.id, recevier_id=receiver.id)

        # When
        accept_friend_request(user_id=receiver.id, request_id=friend_request.id)

        # Then
        self.assertEqual(sender.id, receiver.friends.all()[0].id)
        self.assertEqual(receiver.id, sender.friends.all()[0].id)
        with self.assertRaises(FriendRequest.DoesNotExist):
            FriendRequest.objects.get(id=friend_request.id)

    def test_decline_friend_request(self) -> None:

        # Given
        sender = create_single_user(email="test@test.com", nickname="testuser1", password="testuser1", bio="testuser1")
        receiver = create_single_user(email="test2@test.com", nickname="testuser2", password="testuser2", bio="testuser2")
        friend_request, is_created = send_friend_request(sender_id=sender.id, recevier_id=receiver.id)

        # When
        decline_friend_request(request_id=friend_request.id)

        # Then
        self.assertEqual(0, sender.friends.all().count())
        self.assertEqual(0, receiver.friends.all().count())
        with self.assertRaises(FriendRequest.DoesNotExist):
            FriendRequest.objects.get(id=friend_request.id)

    def test_check_authentication(self) -> None:

        # Given
        user = create_single_user(email="test@test.com", nickname="testuser1", password="testuser1", bio="testuser1")
        password = "testuser1"

        # When
        me = check_authentication(user_id=user.id, password=password)

        # Then
        self.assertTrue(me)
        

    def test_service_profile_delete(self) -> None:

        # Given
        user = create_single_user(email="test@test.com", nickname="testuser1", password="testuser1", bio="testuser1")

        # When
        accounts_profile_delete(user_id=user.id)

        all_users = CustomUser.objects.all()

        # Then
        self.assertEqual(0, all_users.count())

    def test_service_friend_delete(self) -> None:

        # Given
        user = create_single_user(email="test@test.com", nickname="testuser1", password="testuser1", bio="testuser1")
        friend = create_single_user(email="test2@test.com", nickname="testuser2", password="testuser2", bio="testuser2")
        user.friends.add(friend)
        friend.friends.add(user)

        self.assertEqual(1, user.friends.count())
        self.assertEqual(1, friend.friends.count())

        # When
        accounts_delete_friend(user_id=user.id, friend_id=friend.id)

        # Then
        self.assertEqual(0, user.friends.count())
        self.assertEqual(0, friend.friends.count())

    def test_service_send_email_verification(self) -> None:

        # Given
        user = create_single_user(email="didrmatjd@gmail.com", nickname="testuser1", password="testuser1", bio="testuser1")
        current_domain = "127.0.0.1"
        mail_title = "[alaltalk] 이메일 인증 링크입니다."

        # When
        result = send_email_verification(user=user, current_domain=current_domain)

        # Then
        self.assertEqual(1, result)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(mail_title, mail.outbox[0].subject)

    def test_service_verified_email_activation(self) -> None:

        # Given
        user = create_single_user(email="didrmatjd@gmail.com", nickname="testuser1", password="testuser1", bio="testuser1")
        current_domain = "127.0.0.1"
        uidb64 = urlsafe_base64_encode(force_bytes(user.id)).encode().decode()
        token = accounts_verify_token.make_token(user)
        send_email_verification(user=user, current_domain=current_domain)
        self.assertFalse(user.is_active)

        # When
        verified_email_activation(uidb64=uidb64, token=token)
        current_user = CustomUser.objects.get(email="didrmatjd@gmail.com")

        # Then
        self.assertTrue(current_user.is_active)


    def test_service_accounts_token_authenticated_when_user_is_none(self) -> None:
        
        # Given
        unvalid_email = 'unvalid@email.com'
        password = 'unvailidpass'

        # When
        token = accounts_token_authenticated(user_email=unvalid_email, user_password=password)
        
        # Then
        self.assertEqual("NOT_REGISTERD", token)
    
    def test_service_accounts_token_authenticated_when_user_is_not_activated(self) -> None:
        
        # Given
        user = create_single_user(email="testuser1@gmail.com", nickname="testuser1", password="testuser1", bio="testuser1")

        # When
        token = accounts_token_authenticated(user_email=user.email, user_password=user.password)
        
        # Then
        self.assertIsNotNone(token)
        self.assertEqual("NOT_ACTIVATED", token)
    
    def test_service_accounts_token_authenticated_when_user_is_activated(self) -> None:
        
        # Given
        user = create_single_user(email="testuser1@gmail.com", nickname="testuser1", password="testuser1", bio="testuser1")        
        user.is_active = True
        user.save()
        
        # When
        token = accounts_token_authenticated(user_email=user.email, user_password="testuser1")
        login_user = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # Then
        self.assertIsNotNone(token)
        self.assertEqual(user.email, login_user['email'])
    
    def test_service_accounts_token_authenticated_when_password_is_wrong(self) -> None:
        
        # Given
        user = create_single_user(email="testuser1@gmail.com", nickname="testuser1", password="testuser1", bio="testuser1")        
        user.is_active = True
        user.save()
        password = "unvalid_pass"
        
        # When
        token = accounts_token_authenticated(user_email=user.email, user_password=password)        

        # Then
        self.assertIsNotNone(token)
        self.assertEqual("UNVALID_PASSWORD", token)
        
    
    def test_friends_search_prefet_related(self) -> None:
        
        # Given
        user = create_single_user(email="testuser@gmail.com", nickname="testuser1", password="testuser1", bio="testuser1")        
        user.is_active = True
        user.save()

        for i in range(1, 21):
            testuser = create_single_user(email=f"testuser{i}@test.com", nickname=f"testuser{i}", password="testuser1", bio="test")
            user.friends.add(testuser)
            testuser.friends.add(user)
            testuser.save()
            user.save()
        
        
        
        # when: not using prefetch_related()
        with self.assertNumQueries(22):
            for user in CustomUser.objects.all():
                print(user.friends.count())

        # when: using prefetch_releated()
        with self.assertNumQueries(2):
            for user in CustomUser.objects.prefetch_related('friends').all():
                print(user.friends.count())
    
    def test_accounts_search_friends(self) -> None:
        
        # Given
        user = create_single_user(email="testuser@gmail.com", nickname="testuser1", password="testuser1", bio="testuser1")        
        user.is_active = True
        user.save()

        for i in range(1, 21):
            testuser = create_single_user(email=f"testuser{i}@test.com", nickname=f"testuser{i}", password="testuser1", bio="test")
            if i > 15:
                user.friends.add(testuser)
                testuser.friends.add(user)
            testuser.save()
            user.save()

        # When
        with self.assertNumQueries(3):
            search_users = accounts_search_friends(user_id=user.id, query="test")

        # Then
        self.assertIsNotNone(search_users)
        self.assertEqual(21, len(search_users))
        for _user in search_users:
            self.assertIn(_user[1], [0,1,2])
