from ninja import Schema


class CrawlingRequest(Schema):
    search_word: str
