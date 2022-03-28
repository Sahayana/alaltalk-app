from typing import Tuple, Dict
from django.views.decorators.csrf import csrf_exempt
from ninja import Router, Form
from ninja.errors import HttpError

from search.apis.v1.schemas import YoutubeLikeResponse, YoutubeLikeRequest, ShoppingLikeResponse, ShoppingLikeRequest, NewsLikeResponse, NewsLikeRequest, BookLikeResponse, BookLikeRequest
from search.service.like_service import do_like_youtube_service, do_like_shopping_service, do_like_news_service, do_like_book_service
from ...models import Youtube
from accounts.models import CustomUser

router = Router(tags=["like"])


@csrf_exempt
@router.post("/youtube", response={201: YoutubeLikeResponse})
def do_like_youtube(request, youtube_dict: YoutubeLikeRequest = Form(...)) -> Tuple[int, Dict]:
    user_id = request.user.id
    try:
        result = do_like_youtube_service(user_id, youtube_dict.url)
    except CustomUser.DoesNotExist:
        raise HttpError(404, f"User is not Exist")
    return 201, {'result': result}


@csrf_exempt
@router.post("/news", response={201: NewsLikeResponse})
def do_like_news(request, News_request: NewsLikeRequest = Form(...)) -> Tuple[int, Dict]:
    try:
        result = do_like_news_service(
            request.user.id,
            title=News_request.title,
            date=News_request.date,
            company=News_request.company,
            content=News_request.content,
            thumbnail_url=News_request.thumbnail,
            link_url=News_request.link
        )
    except CustomUser.DoesNotExist:
        raise HttpError(404, 'User does not exist!!!')
    return 201, {'result': result}


@csrf_exempt
@router.post("/book", response={201: BookLikeResponse})
def do_like_book(request, Book_request: BookLikeRequest = Form(...)) -> Tuple[int, Dict]:
    try:
        result = do_like_book_service(
            request.user.id,
            title=Book_request.title,
            date=Book_request.date,
            company=Book_request.company,
            content=Book_request.content,
            thumbnail_url=Book_request.thumbnail,
            link_url=Book_request.link
        )
    except CustomUser.DoesNotExist:
        raise HttpError(404, 'User does not exist!!!')
    return 201, {'result': result}


@csrf_exempt
@router.post("/shopping", response={201: ShoppingLikeResponse})
def do_like_shopping(request, shopping_request: ShoppingLikeRequest = Form(...)) -> Tuple[int, Dict]:
    try:
        result = do_like_shopping_service(
            request.user.id,
            title=shopping_request.title,
            price=shopping_request.price,
            thumbnail_url=shopping_request.thumbnail,
            link_url=shopping_request.link
        )
    except CustomUser.DoesNotExist:
        raise HttpError(404, 'User does not exist!!!')
    return 201, {'result': result}

