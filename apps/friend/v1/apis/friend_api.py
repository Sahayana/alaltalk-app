import json

from rest_framework import permissions, renderers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.account.services.user_service import UserService
from apps.account.v1.serializers.user_serializer import (
    UserLikeKeywordSerilaizer,
    UserReadSerializer,
)
from apps.friend.models import Friend
from apps.friend.services.friend_selector import FriendSelector
from apps.friend.services.friend_service import FriendService
from apps.friend.v1.serializers.friend_serializer import FriendSerializer


class FriendViewSet(viewsets.ModelViewSet):

    queryset = Friend.objects.select_related("user", "target_user").all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendSerializer

    def get_renderers(self):
        if self.action == "list":
            renderer_classes = [renderers.TemplateHTMLRenderer]
        else:
            renderer_classes = [renderers.JSONRenderer]
        return [renderer() for renderer in renderer_classes]

    def list(self, request, *args, **kwargs):
        """현재 친구 목록과 추천 친구를 렌더링합니다."""
        user = request.user
        context = {
            "user": user,
            "friends": FriendSelector.get_friends_list(user_id=user.id),
            "recommend_friend": FriendService.recommend_friend(user=user),
        }

        return Response(
            context, template_name="account/user_list.html", status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        """
        친구 상태를 해제합니다.
        """
        obj = self.get_object()
        user = request.user
        target_user = obj.target_user

        friend = FriendService.disconnect_friend(
            user_id=user.id, target_user_id=target_user.id
        )

        data = {"msg": "deleted", "data": self.get_serializer(friend).data}

        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def search(self, request, *args, **kwargs):
        """유저 혹은 친구를 검색합니다."""
        user = request.user
        query = request.query_params.get("q")

        friends = FriendSelector.search_friend(user_id=user.id, query=query)
        serializer = UserReadSerializer(friends, many=True)

        data = {"result": serializer.data}

        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def keyword(self, request, *args, **kwargs):
        """
        유저의 관심 키워드를 저장합니다.
        """
        user = request.user
        keyword = json.loads(request.body.decode("utf-8"))["like_keyword"]

        user_keyword = UserService.save_like_keyword(user_id=user.id, keyword=keyword)
        data = {"msg": "add like", "data": UserLikeKeywordSerilaizer(user_keyword).data}

        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def recommend_keywords(self, request, *args, **kwargs):
        """
        채팅방에서 대화하는 친구의 관심 키워드를 최신순으로 '최대 3개' 노출합니다.
        """
        target_user_id = int(request.data.get("target_user_id"))
        keywords = FriendService.friend_like_recommend(target_user_id=target_user_id)
        data = {"keywords": keywords}

        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def get_user_like(self, request, *args, **kwargs):
        user = request.user
        like_sentence = FriendService.get_user_like_data(user_id=user.id)
        data = {"like_sentence": like_sentence}

        return Response(data=data, status=status.HTTP_200_OK)
