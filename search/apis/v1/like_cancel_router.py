from typing import Tuple, Dict

from django.views.decorators.csrf import csrf_exempt
from ninja import Router, Form
from search.service.like_cancel_service import like_cancel_youtube
from search.apis.v1.schemas import YoutubeLikeRequest, YoutubeLikeResponse
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
@router.post("/news")
def cancel_like_shopping(request):
    return 0


@csrf_exempt
@router.post("/book")
def do_like_book(request):
    return 0


@csrf_exempt
@router.post("/shopping")
def do_like_shopping(request):
    return 0


