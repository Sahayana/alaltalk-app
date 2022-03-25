from typing import Dict, List, Tuple

from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ninja import Form, Router

from ...functions import crawling_youtube, crawling_shopping_only_bs4
from search.service.search_service import crawling_news, crawling_book
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
    all_response["news"] = crawling_news(crawling_request.target)
    all_response["shopping"] = crawling_shopping_only_bs4(crawling_request.target, content_count)
    all_response["book"] = crawling_book(crawling_request.target)
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


# like API
@csrf_exempt
@router.post("/like/news")
def do_like_news(request):
    # 1. Javascript로 id='test'인 기사 데이터를 ajax를 통해 보내기 ( 제목, 시간, 신문사, 내용, 썸네일 )
    # 2. 해당 함수에서 ajxax 연결 확인
    # 3. DB 데이터 유저 조회 - request.user
    # 4. News 모델 새로 만들기 > 유저 foreignkey 로 넣기
    return 0


@csrf_exempt
@router.post("/cancel_like/news")
def cancel_like_news(request):
    return 0


@csrf_exempt
@router.post("/like/youtube")
def do_like_youtube(request):
    return 0


@csrf_exempt
@router.post("/cancel_like/youtube")
def cancel_like_youtube(request):
    return 0

@csrf_exempt
@router.post("/like/book")
def do_like_book(request):
    return 0


@csrf_exempt
@router.post("/cancel_like/book")
def cancel_like_book(request):
    return 0


@csrf_exempt
@router.post("/like/shopping")
def do_like_shopping(request):
    return 0


@csrf_exempt
@router.post("/cancel_like/shopping")
def cancel_like_shopping(request):
    return 0