from django.http import HttpRequest
from ninja import Router, Form
from ...functions import crawling_youtube
from typing import List, Tuple, Dict
from .schemas import CrawlingRequest, CrawlingResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

router = Router(tags=["search"])


@csrf_exempt
@router.get("/")
def open_test(request):
    return render(request, 'base.html')


@csrf_exempt
@router.post("/crawling", response={201: CrawlingResponse})
def recommend_contents(request: HttpRequest, crawling_request: CrawlingRequest = Form(...)) -> Tuple[int, Dict]:
    all_response = {}
    content_count = 10
    all_response['youtube'] = crawling_youtube(crawling_request.target, content_count)
    return 201, {'all_response': all_response}

