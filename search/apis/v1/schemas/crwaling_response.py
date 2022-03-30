from typing import Dict, List

from ninja import Schema


class CrawlingResponse(Schema):
    all_response: Dict


class SearchResponse(Schema):
    result: List[List[str]]
