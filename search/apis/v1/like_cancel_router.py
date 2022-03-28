from typing import Tuple, Dict

from django.views.decorators.csrf import csrf_exempt
from ninja import Router, Form
from search.service.like_cancel_service import like_cancel_youtube
from search.apis.v1.schemas import YoutubeLikeRequest, YoutubeLikeResponse, ShoppingLikeResponse, ShoppingLikeResponse, NewsLikeResponse, NewsLikeResponse, BookLikeResponse, BookLikeResponse
from search.models import Youtube, Book, News, Shopping
from accounts.models import CustomUser
from ninja.errors import HttpError


router = Router(tags=["like_cancel"])


@csrf_exempt
@router.post("/youtube", response={201: YoutubeLikeResponse})
def cancel_like_youtube(request, youtube_request: YoutubeLikeRequest = Form(...)) -> Tuple[int, Dict]:
    try:
        like_cancel_youtube(request.user.id, youtube_request.url)
    except CustomUser.DoesNotExist:
        raise HttpError(404, 'User does not Exist')
    except Youtube.DoesNotExist:
        raise HttpError(404, 'Youtube does not Exist')
    return 201, {'result': 'success'}


@csrf_exempt
@router.post("/news", response={201: NewsLikeResponse})
def cancel_like_shopping(request, news_request: NewsLikeRequest = Form(...)) -> Tuple[int, Dict]:):
    try:
        like_cancel_news(request.user.id, news_request.url)
    except CustomUser.DoesNotExist:
        raise HttpError(404, 'User does not Exist')
    except News.DoesNotExist:
        raise HttpError(404, 'News does not Exist')
    return 201, {'result': 'success'}


@csrf_exempt
@router.post("/book", response={201: BookLikeResponse})
def do_like_book(request, book_request: BookRequest = Form(...)) -> Tuple[int, Dict]:):
    try:
        like_cancel_book(request.user.id, book_request.url)
    except CustomUser.DoesNotExist:
        raise HttpError(404, 'User does not Exist')
    except Book.DoesNotExist:
        raise HttpError(404, 'Book does not Exist')
    return 201, {'result': 'success'}


@csrf_exempt
@router.post("/shopping", response={201: ShoppingLikeResponse})
def do_like_shopping(request, shopping_request: ShoppingLikeRequest = Form(...)) -> Tuple[int, Dict]:):
    try:
        like_cancel_shopping(request.user.id, shopping_request.url)
    except CustomUser.DoesNotExist:
        raise HttpError(404, 'User does not Exist')
    except Shopping.DoesNotExist:
        raise HttpError(404, 'Shopping does not Exist')
    return 201, {'result': 'success'}


