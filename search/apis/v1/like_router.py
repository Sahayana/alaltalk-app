from typing import Tuple, Dict
from django.views.decorators.csrf import csrf_exempt
from ninja import Router
from ninja.errors import HttpError

from search.apis.v1.schemas import YoutubeLikeResponse, YoutubeLikeRequest
from search.service.like_service import do_like_youtube_service
from ...models import Youtube
from accounts.models import CustomUser

router = Router(tags=["like"])


@csrf_exempt
@router.post("/youtube", response={201: YoutubeLikeResponse})
def do_like_youtube(request, youtube_dict: YoutubeLikeRequest) -> Tuple[int, Dict]:
    user_id = request.user.id
    try:
        result = do_like_youtube_service(user_id, youtube_dict)
    except CustomUser.DoesNotExist:
        raise HttpError(404, f"User is not Exist")
    return 201, {'result': result}


@csrf_exempt
@router.post("/news")
def do_like_book(request):
    return 0


@csrf_exempt
@router.post("/book")
def do_like_book(request):
    return 0


@csrf_exempt
@router.post("/shopping")
def do_like_shopping(request):
    return 0

