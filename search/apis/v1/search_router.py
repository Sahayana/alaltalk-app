from typing import Dict, List, Tuple

from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ninja import Form, Router

from ...functions import crawling_youtube
from .schemas import CrawlingRequest, CrawlingResponse

router = Router(tags=["search"])


@csrf_exempt
@router.get("/")
def open_test(request):
    return render(request, "base.html")


@csrf_exempt
@router.post("/crawling", response={201: CrawlingResponse})
def recommend_contents(request: HttpRequest, crawling_request: CrawlingRequest = Form(...)) -> Tuple[int, Dict]:
    all_response = {}
    content_count = 10
    all_response["youtube"] = crawling_youtube(crawling_request.target, content_count)
    return 201, {"all_response": all_response}


@csrf_exempt
@router.get("/chat")
def open_chat_room(request):
    return render(request, "search/recommend_include_chatroom.html")


@csrf_exempt
@router.get("/recommend")
def open_chat_room(request):
    return render(request, "search/recommend_include_recommend.html")


@csrf_exempt
@router.get("/chat_list")
def open_chat_room(request):
    return render(request, "search/recommend_include_chat_list.html")


@csrf_exempt
@router.get("/spinner")
def open_chat_room(request):
    return render(request, "search/recommend_spinner.html")
