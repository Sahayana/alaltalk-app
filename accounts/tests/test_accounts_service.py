from django.test import TestCase
from accounts.services.accounts_service import create_single_user, check_email_duplication, get_friend_list
from django.contrib.auth.hashers import check_password


class AccountsTest(TestCase):
    
    def test_create_a_single_user(self) -> None:
        # Given
        email = "test@test.com"
        nickname = "testuser1"
        password = "testuser1"
        bio = 'testuser1'

        # When
        user = create_single_user(email=email, nickname=nickname, password=password, bio=bio)
        
        # Then
        self.assertEqual(1, user.id)
        self.assertEqual('testuser1', user.bio)
        
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