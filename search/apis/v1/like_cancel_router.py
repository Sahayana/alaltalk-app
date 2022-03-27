from typing import Tuple, Dict

from django.views.decorators.csrf import csrf_exempt
from ninja import Router

router = Router(tags=["like_cancel"])


@csrf_exempt
@router.post("/youtube")
def cancel_like_youtube(request):
    return 0


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


