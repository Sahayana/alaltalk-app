from django.http import HttpRequest
from ninja import Router
from ...functions import crawling_youtube
from typing import List, Tuple, Dict
from .schemas import CrawlingRequest, CrawlingResponse

router = Router(tags=["search"])


@router.post("/", response={200: CrawlingResponse})
def recommend_contents(request: HttpRequest, recommend_request: CrawlingRequest) -> Tuple[int, Dict]:
    all_response = {}
    content_count = 10
    all_response['youtube'] = crawling_youtube(recommend_request.search_word, content_count)
    print(all_response)
    return 200, {'all_response': all_response}

