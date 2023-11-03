from ninja import Schema


class CrawlingRequest(Schema):
    target: str


class SearchRequest(Schema):
    search: str
