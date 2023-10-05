import factory
from django.core.files.base import ContentFile

from apps.account.constants import DEFAULT_IMG
from apps.account.models import CustomUser, UserLikeKeyWord, UserProfileImage
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
    def password(self, create, extracted, **kwargs):
        if extracted:
            self.set_password(extracted)
        else:
            self.set_password("alaltalk!")


class UserProfileImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfileImage

    user = factory.SubFactory(factory=UserFactory)
    img = factory.LazyAttribute(
        lambda o: ContentFile(
            factory.django.ImageField()._make_data({"width": 1024, "height": 768}),
            "test.jpg",
        )
    )


class UserLikeKeywordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserLikeKeyWord

    user = factory.SubFactory(factory=UserFactory)
    keyword = factory.Faker(provider="job", locale="ko_KR")
