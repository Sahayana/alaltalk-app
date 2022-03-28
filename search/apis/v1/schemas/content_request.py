from ninja import Schema


class YoutubeLikeRequest(Schema):
    url: str


class ShoppingLikeRequest(Schema):
    title: str
    link: str
    price: str
    thumbnail: str
