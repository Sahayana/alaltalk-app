from typing import Dict, Tuple

from accounts.models import CustomUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ninja import Form, Router
from ninja.errors import HttpError
from search.apis.v1.schemas import (
    BookLikeRequest,
    BookLikeResponse,
    NewsLikeRequest,
    NewsLikeResponse,
    ShoppingLikeRequest,
    ShoppingLikeResponse,
    YoutubeLikeRequest,
    YoutubeLikeResponse,
)
from search.models import Book, News, Shopping, Youtube
from search.service.like_cancel_service import (
    like_cancel_book,
    like_cancel_news,
    like_cancel_shopping,
    like_cancel_youtube,
)

router = Router(tags=["like_cancel"])


@router.post("/youtube", response={201: YoutubeLikeResponse})
def cancel_like_youtube(
    request, youtube_request: YoutubeLikeRequest = Form(...)
) -> Tuple[int, Dict]:
    try:
        like_cancel_youtube(request.user.id, youtube_request.url)
    except CustomUser.DoesNotExist:
        raise HttpError(404, "User does not Exist")
    except Youtube.DoesNotExist:
        raise HttpError(404, "Youtube does not Exist")
    return 201, {"result": "success"}


@router.post("/news", response={201: NewsLikeResponse})
def cancel_like_news(
    request, news_request: NewsLikeRequest = Form(...)
) -> Tuple[int, Dict]:
    try:
        like_cancel_news(user_id=request.user.id, news_url=news_request.link)
    except CustomUser.DoesNotExist:
        raise HttpError(404, "User does not Exist")
    except News.DoesNotExist:
        raise HttpError(404, "News does not Exist")
    return 201, {"result": "success"}


@router.post("/book", response={201: BookLikeResponse})
def cancel_like_book(
    request, book_request: BookLikeRequest = Form(...)
) -> Tuple[int, Dict]:
    try:
        like_cancel_book(user_id=request.user.id, book_url=book_request.link)
    except CustomUser.DoesNotExist:
        raise HttpError(404, "User does not exist")
    except Book.DoesNotExist:
        raise HttpError(404, "Book does not exist")
    return 201, {"result": "success"}


@router.post("/shopping", response={201: ShoppingLikeResponse})
def cancel_like_shopping(request, shopping_request: ShoppingLikeRequest = Form(...)):
    try:
        like_cancel_shopping(
            user_id=request.user.id, shopping_url=shopping_request.link
        )
    except CustomUser.DoesNotExist:
        raise HttpError(404, "User does not Exist")
    except Shopping.DoesNotExist:
        raise HttpError(404, "Shopping does not Exist")
    return 201, {"result": "success"}
