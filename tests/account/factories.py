import factory

from apps.account.constants import DEFAULT_IMG
from apps.account.models import CustomUser, UserProfileImage
from apps.account.utils import random_string_generator


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.LazyAttribute(
        lambda o: f"{random_string_generator(7)}@alaltalk.com"
    )
    nickname = factory.LazyAttribute(lambda o: o.email.split("@")[0])
    bio = factory.LazyAttribute(lambda o: o.email.split("@")[0])

    @factory.post_generation
    def user_profile_imgs(self, create, extracted, **kwargs):
        if not create:
            return None
        if extracted:
            self.user_profile_imgs.add(extracted)
            self.save()

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if extracted:
            self.set_password(extracted)
        else:
            self.set_password("alaltalk")
        self.save()


class UserProfileImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfileImage

    user = factory.SubFactory(factory=UserFactory, user_profile_imgs=None)
    img = DEFAULT_IMG
