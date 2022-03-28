from typing import Dict, Tuple

from django.views.decorators.csrf import csrf_exempt
from ninja import Form, Router
from ninja.errors import HttpError
from accounts.models import CustomUser

from search.apis.v1.schemas import (
    ShoppingLikeRequest,
    ShoppingLikeResponse,
    YoutubeLikeRequest,
    YoutubeLikeResponse,
)
from search.service.like_service import (
    do_like_shopping_service,
    do_like_youtube_service,
)

<<<<<<< HEAD
from search.apis.v1.schemas import YoutubeLikeResponse, YoutubeLikeRequest, ShoppingLikeResponse, ShoppingLikeRequest, NewsLikeResponse, NewsLikeRequest, BookLikeResponse, BookLikeRequest
from search.service.like_service import do_like_youtube_service, do_like_shopping_service, do_like_news_service, do_like_book_service
=======
from search.apis.v1.schemas import YoutubeLikeResponse, YoutubeLikeRequest, ShoppingLikeResponse, ShoppingLikeRequest
from search.apis.v1.schemas import BookLikeResponse, BookLikeRequest
from search.service.like_service import do_like_youtube_service, do_like_shopping_service, do_like_book_service

>>>>>>> 5562c7502d752756ea5430a53ce5772787b5c321
from ...models import Youtube

router = Router(tags=["like"])


@csrf_exempt
@router.post("/youtube", response={201: YoutubeLikeResponse})
def do_like_youtube(request, youtube_dict: YoutubeLikeRequest = Form(...)) -> Tuple[int, Dict]:
    user_id = request.user.id
    try:
        result = do_like_youtube_service(user_id, youtube_dict.url)
    except CustomUser.DoesNotExist:
        raise HttpError(404, f"User is not Exist")
    return 201, {"result": result}


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
<<<<<<< HEAD
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
=======
def do_like_book(request, book_request: BookLikeRequest = Form(...)) -> Tuple[int, Dict]:
    try:
        result = do_like_book_service(
            user_id=request.user.id,
            title=book_request.title,
            price=book_request.price,
            author=book_request.author,
            company=book_request.company,
            thumbnail=book_request.thumbnail,
            link=book_request.link
        )
    except CustomUser.DoesNotExist:
        raise HttpError(404, 'User does not exist!')
>>>>>>> 5562c7502d752756ea5430a53ce5772787b5c321
    return 201, {'result': result}


@csrf_exempt
@router.post("/shopping", response={201: ShoppingLikeResponse})
def do_like_shopping(request, shopping_request: ShoppingLikeRequest = Form(...)) -> Tuple[int, Dict]:
    try:
        result = do_like_shopping_service(
            user_id=request.user.id,
            title=shopping_request.title,
            price=shopping_request.price,
            thumbnail_url=shopping_request.thumbnail,
            link_url=shopping_request.link
        )
    except CustomUser.DoesNotExist:
        raise HttpError(404, 'User does not exist!!!')
    return 201, {'result': result}

