from ninja import Router
from django.http import JsonResponse
from search.models import Youtube, News, Book, Shopping


router = Router(tags=["chat_room"])


@router.post("/youtube")
def create_chat_room(request) -> JsonResponse:
    youtube_id = request.POST['id']
    friend_youtube = Youtube.objects.get(pk=youtube_id)
    friend_youtube.pk = None
    friend_youtube.user_id = request.user.id
    if Youtube.objects.filter(user=request.user.id, url=friend_youtube.url).exists():
        result = 'AlreadyExist'
    else:
        result = 'success'
        friend_youtube.save()
    data = {
        'result': result
    }
    return JsonResponse(data)


@router.post("/news")
def create_chat_room(request) -> JsonResponse:
    news_id = request.POST['id']
    friend_news = News.objects.get(pk=news_id)
    friend_news.pk = None
    friend_news.user_id = request.user.id
    if News.objects.filter(user=request.user.id, link=friend_news.link).exists():
        result = 'AlreadyExist'
    else:
        result = 'success'
        friend_news.save()
    data = {
        'result': result
    }
    return JsonResponse(data)


@router.post("/book")
def create_chat_room(request) -> JsonResponse:
    book_id = request.POST['id']
    friend_book = Book.objects.get(pk=book_id)
    friend_book.pk = None
    friend_book.user_id = request.user.id
    if Book.objects.filter(user=request.user.id, link=friend_book.link).exists():
        result = 'AlreadyExist'
    else:
        result = 'success'
        friend_book.save()
    data = {
        'result': result
    }
    return JsonResponse(data)


@router.post("/shopping")
def create_chat_room(request) -> JsonResponse:
    shopping_id = request.POST['id']
    friend_shopping = Shopping.objects.get(pk=shopping_id)
    friend_shopping.pk = None
    friend_shopping.user_id = request.user.id
    if Shopping.objects.filter(user=request.user.id, link=friend_shopping.link).exists():
        result = 'AlreadyExist'
    else:
        result = 'success'
        friend_shopping.save()
    data = {
        'result': result
    }
    return JsonResponse(data)
