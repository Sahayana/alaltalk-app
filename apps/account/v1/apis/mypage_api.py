from django.core.cache import cache
from rest_framework import permissions, renderers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from alaltalk import cache_key
from apps.account.models import CustomUser, UserProfileImage
from apps.account.services.user_service import UserService
from apps.account.v1.serializers.user_serializer import (
    UserProfileImageSerializer,
    UserReadSerializer,
    UserUpdateSerializer,
)
from apps.friend.services.friend_selector import FriendSelector


class MyPageViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            CustomUser.objects.filter(is_deleted=False)
            .filter(id=self.request.user.id)
            .prefetch_related("youtube", "news", "book", "shopping")
        )

    def get_renderers(self):
        if self.action == "list":
            renderer_classes = [renderers.TemplateHTMLRenderer]
        else:
            renderer_classes = [renderers.JSONRenderer]
        return [renderer() for renderer in renderer_classes]

    def get_serializer_class(self):

        if self.action == "list":
            serializer_class = UserReadSerializer
        elif self.action == "create":
            serializer_class = UserUpdateSerializer
        return serializer_class

    def list(self, request, *args, **kwargs):
        """유저의 마이페이지를 렌더링 합니다."""

        user = request.user
        friend_requests = FriendSelector.get_recieved_requests(user_id=user.id)
        youtubes = cache.get_or_set(
            cache_key.USER_YOUTUBE.format(user_id=user.id),
            self.get_queryset().get().youtube.all(),
            timeout=86400,
        )
        news = cache.get_or_set(
            cache_key.USER_NEWS.format(user_id=user.id),
            self.get_queryset().get().news.all(),
            timeout=86400,
        )
        books = cache.get_or_set(
            cache_key.USER_BOOK.format(user_id=user.id),
            self.get_queryset().get().book.all(),
            timeout=86400,
        )
        shoppings = cache.get_or_set(
            cache_key.USER_SHOPPING.format(user_id=user.id),
            self.get_queryset().get().shopping.all(),
            timeout=86400,
        )

        context = {
            "user": user,
            "friend_requests": friend_requests,
            "youtubes": youtubes,
            "news": news,
            "books": books,
            "shoppings": shoppings,
        }

        return Response(
            context, status=status.HTTP_200_OK, template_name="account/mypage.html"
        )

    def create(self, request, *args, **kwargs):
        """회원 정보를 업데이트 합니다."""

        user = request.user
        serializer = self.get_serializer(instance=user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            data = {"msg": "ok", "data": UserReadSerializer(instance=user).data}

            return Response(data=data, status=status.HTTP_200_OK)
        return Response(
            data=serializer.error_messages, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, *args, **kwargs):
        """회원 탈퇴"""
        user = UserService.delete_user_account(user_id=request.user.id)
        data = {"msg": "deleted", "data": UserReadSerializer(user).data}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def auth_check(self, request, *args, **kwargs):
        user = request.user
        password = request.data.get("password")

        if user.check_password(password):
            return Response(data={"msg": "ok"}, status=status.HTTP_200_OK)
        return Response(data={"msg": "no"}, status=status.HTTP_400_BAD_REQUEST)
