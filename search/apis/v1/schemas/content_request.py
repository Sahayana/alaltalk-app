from ninja import Schema


class YoutubeLikeRequest(Schema):
    url: str
