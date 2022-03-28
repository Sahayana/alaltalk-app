from typing import Dict, Tuple

from django.views.decorators.csrf import csrf_exempt
from ninja import Form, Router
from ninja.errors import HttpError

<<<<<<< HEAD
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

=======
from accounts.models import CustomUser
from search.apis.v1.schemas import YoutubeLikeRequest, YoutubeLikeResponse
from search.service.like_service import do_like_youtube_service

>>>>>>> accounts
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
@router.post("/news")
def do_like_book(request):
    return 0


@csrf_exempt
@router.post("/book")
def do_like_book(request):
    return 0


@csrf_exempt
<<<<<<< HEAD
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

=======
@router.post("/shopping")
def do_like_shopping(request):
    return 0
>>>>>>> accounts
