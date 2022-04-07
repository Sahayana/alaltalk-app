from typing import Dict, List, Tuple
from django.http import JsonResponse
from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ninja import Form, Router
from search.models import Book, News, Shopping, Youtube
from search.service.search_service import crawling_book, crawling_news
from accounts.models import CustomUser
from ...functions import crawling_shopping_only_bs4, crawling_youtube
from .schemas import CrawlingRequest, CrawlingResponse, SearchRequest, SearchResponse

router = Router(tags=["search"])


# Page Load API
@csrf_exempt
@router.get("/chat")
def open_chat_room(request):
    return render(request, "search/recommend_include_chatroom.html")


@csrf_exempt
@router.get("/recommend")
def open_chat_room(request):
    return render(request, "search/recommend_include_recommend.html", {'user': request.user})


@csrf_exempt
@router.get("/chat_list")
def open_chat_room(request):
    return render(request, "search/recommend_include_chat_list.html")


# Crawling  API
@csrf_exempt
@router.post("/crawling", response={201: CrawlingResponse})
def recommend_contents(request: HttpRequest, crawling_request: CrawlingRequest = Form(...)) -> Tuple[int, Dict]:
    all_response = {}
    content_count = 10
    try:
        all_response["youtube"] = crawling_youtube(crawling_request.target, content_count)
        for youtube_row in all_response['youtube']:
            if Youtube.objects.filter(user=request.user.id, url=youtube_row[0]).exists():
                youtube_row[4] = 'True'
    except Exception as e:
        print('youtube_crawling Error: ', e)
        all_response["youtube"] = []
    try:
        all_response["news"] = crawling_news(crawling_request.target)
        for news_row in all_response['news']:
            if News.objects.filter(user=request.user.id, link=news_row[3]).exists():
                news_row[6] = 'True'
    except Exception as e:
        print('news_crawling Error: ', e)
        all_response["news"] = []
    try:
        all_response["shopping"] = crawling_shopping_only_bs4(crawling_request.target, content_count)
        for shopping_row in all_response['shopping']:
            if Shopping.objects.filter(user=request.user.id, link=shopping_row[3]).exists():
                shopping_row[4] = 'True'
    except Exception as e:
        print('shopping_crawling Error: ', e)
        all_response["shopping"] = []
    try:
        all_response["book"] = crawling_book(crawling_request.target)
        for news_row in all_response['book']:
            if Book.objects.filter(user=request.user.id, link=news_row[5]).exists():
                news_row[7] = 'True'
    except Exception as e:
        print('book_crawling Error: ', e)
        all_response['book'] = []
    return 201, {"all_response": all_response}


# Search API
@csrf_exempt
@router.post('/youtube', response={201: SearchResponse})
def search_youtube(request, youtube_request: SearchRequest = Form(...)) -> Tuple[int, Dict]:
    content_count = 10
    youtube_list = []
    print(youtube_request.search)
    try:
        youtube_list = crawling_youtube(youtube_request.search, content_count)
        for youtube_row in youtube_list:
            if Youtube.objects.filter(user=request.user.id, url=youtube_row[0]).exists():
                youtube_row[4] = 'True'

    except Exception as e:
        print('Search_youtube is Error:', e)

    return 201, {'result': youtube_list}


@csrf_exempt
@router.post('/news', response={201: SearchResponse})
def search_news(request, news_request: SearchRequest = Form(...)) -> Tuple[int, Dict]:
    news_list = []
    try:
        news_list = crawling_news(news_request.search)
        for news_row in news_list:
            if News.objects.filter(user=request.user.id, link=news_row[3]).exists():
                news_row[6] = 'True'
    except Exception as e:
        print('news_crawling Error: ', e)

    return 201, {'result': news_list}


@csrf_exempt
@router.post('/book', response={201: SearchResponse})
def search_book(request, book_request: SearchRequest = Form(...)) -> Tuple[int, Dict]:
    book_list = []
    try:
        book_list = crawling_book(book_request.search)
        for book_row in book_list:
            if Book.objects.filter(user=request.user.id, link=book_row[5]).exists():
                book_row[7] = 'True'
    except Exception as e:
        print('book_crawling Error: ', e)

    return 201, {'result': book_list}


@csrf_exempt
@router.post('/shopping', response={201: SearchResponse})
def search_shopping(request, shopping_request: SearchRequest = Form(...)) -> Tuple[int, Dict]:
    content_count = 10
    shopping_list = []
    try:
        shopping_list = crawling_shopping_only_bs4(shopping_request.search, content_count)
        for shopping_row in shopping_list:
            if Shopping.objects.filter(user=request.user.id, link=shopping_row[3]).exists():
                shopping_row[4] = 'True'
    except Exception as e:
        print('shopping_crawling Error: ', e)

    return 201, {'result': shopping_list}


@csrf_exempt
@router.post('/recommend_change')
def recommend_on_off_switch(request):
    recommend_state = request.POST['value']

    if recommend_state == 'false':
        recommend_state = False
    elif recommend_state == 'true':
        recommend_state=True
    else:
        return JsonResponse({'result': 'Not boolean!'})
    print('recommend_state: ', recommend_state)
    user = CustomUser.objects.get(id=request.user.id)
    user.is_recommend_on = recommend_state
    user.save()
    data = {
        'result': 'save'
    }
    return JsonResponse(data)
