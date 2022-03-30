from typing import Dict, List, Tuple

from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ninja import Form, Router

from search.models import Book, News, Shopping, Youtube
from search.service.search_service import crawling_book, crawling_news

from ...functions import crawling_shopping_only_bs4, crawling_youtube
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
    try:
        all_response["youtube"] = crawling_youtube(crawling_request.target, content_count)
        for youtube_row in all_response['youtube']:
            if Youtube.objects.filter(user=request.user.id, url=youtube_row[0]).exists():
                youtube_row[4] = True
    except Exception as e:
        print('youtube_crawling Error: ', e)
        all_response["youtube"] = []
    try:
        all_response["news"] = crawling_news(crawling_request.target)
        for news_row in all_response['news']:
            if News.objects.filter(user=request.user.id, link=news_row[3]).exists():
                news_row[6] = True
    except Exception as e:
        print('news_crawling Error: ', e)
        all_response["news"] = []
    try:
        all_response["shopping"] = crawling_shopping_only_bs4(crawling_request.target, content_count)
        for shopping_row in all_response['shopping']:
            if Shopping.objects.filter(user=request.user.id, link=shopping_row[3]).exists():
                shopping_row[4] = True
    except Exception as e:
        print('shopping_crawling Error: ', e)
        all_response["shopping"] = []
    try:
        all_response["book"] = crawling_book(crawling_request.target)
        for news_row in all_response['book']:
            if Book.objects.filter(user=request.user.id, link=news_row[5]).exists():
                news_row[7] = True
    except Exception as e:
        print('book_crawling Error: ', e)
        all_response['book'] = []
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
