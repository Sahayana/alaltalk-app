from ninja import Schema


class CrawlingRequest(Schema):
    target: str
