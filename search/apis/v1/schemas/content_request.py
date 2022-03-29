from ninja import Schema


class YoutubeLikeRequest(Schema):
    url: str


class ShoppingLikeRequest(Schema):
    title: str
    link: str
    price: str
    thumbnail: str


class NewsLikeRequest(Schema):
    title: str
    date: str
    link: str
    company: str
    content: str
    thumbnail: str


class BookLikeRequest(Schema):
    title: str
    price: str
    link: str
    company: str
    author: str
    thumbnail: str

