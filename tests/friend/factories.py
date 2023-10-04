import factory

from apps.friend.models import Friend, FriendRequest
from tests.account.factories import UserFactory


class FriendRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FriendRequest

    user = factory.SubFactory(UserFactory)
    target_user = factory.SubFactory(UserFactory)


class FriendFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Friend

    user = factory.SubFactory(UserFactory)
    target_user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def friends(self, created, extracted, **kwargs):
        if created:
            self.user.friends.add(self.target_user)
            self.target_user.friends.add(self.user)
            self.save()
        return