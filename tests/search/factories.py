import factory
from factory.faker import faker

from apps.account.utils import random_string_generator
from apps.search.models import Book, News, Shopping, Youtube
from tests.account.factories import UserFactory

fake = faker.Faker()


class YoutubeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Youtube

    user = factory.SubFactory(UserFactory)
    url = factory.LazyAttribute(
        lambda o: f"https://youtube.com/{random_string_generator(10)}"
    )
    title = factory.Faker(provider="sentence", locale="en_US", nb_words=5)
    views = "100"


class NewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = News

    user = factory.SubFactory(UserFactory)
    title = factory.Faker(provider="sentence", nb_words=10, locale="en_US")
    date = "2023-11-08"
    company = factory.Faker(provider="company", locale="ko_KR")
    thumbnail = fake.image_url()
    link = factory.LazyAttribute(
        lambda o: faker.Faker().url() + f"{random_string_generator(10)}"
    )

    @factory.lazy_attribute
    def content(self):
        c = ""
        for _ in range(0, 5):
            c += "\n" + fake.paragraph(nb_sentences=10) + "\n"
        return c


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    user = factory.SubFactory(UserFactory)
    title = factory.Faker(provider="sentence", locale="en_US", nb_words=2)
    price = "15000"
    author = factory.Faker(provider="name", locale="ko_KR")
    company = factory.Faker(provider="company", locale="ko_KR")
    thumbnail = fake.image_url()
    link = factory.LazyAttribute(
        lambda o: faker.Faker().url() + f"{random_string_generator(10)}"
    )
    series = "fantasy"


class ShoppingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Shopping

    user = factory.SubFactory(UserFactory)
    price = "15000"
    thumbnail = fake.image_url()
    link = factory.LazyAttribute(
        lambda o: faker.Faker().url() + f"{random_string_generator(10)}"
    )
    title = factory.Faker(provider="sentence", locale="en_US", nb_words=2)
