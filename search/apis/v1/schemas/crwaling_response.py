from typing import Dict

from ninja import Schema


class CrawlingResponse(Schema):
    all_response: Dict
