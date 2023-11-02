import json

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.account.services.user_service import UserService
from apps.account.v1.serializers.user_serializer import UserLikeKeywordSerilaizer
from apps.friend.models import Friend
from apps.friend.services.friend_service import FriendService
from apps.friend.v1.serializers.friend_serializer import FriendSerializer
from apps.pagination import CommonPagination


class FriendViewSet(viewsets.ModelViewSet):

    queryset = Friend.objects.select_related("user", "target_user").all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendSerializer

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

    # @action(detail=False, methods=["post"])
    # def get_user_like(self, request, *args, **kwargs):
    #     user = request.user
    #     like_sentence = []
    #     sentence = ""
    #     youtube = Youtube.objects.filter(user_id=user.id)
    #     news = News.objects.filter(user_id=user.id)
    #     book = Book.objects.filter(user_id=user.id)
    #     shopping = Shopping.objects.filter(user_id=user.id)

    #     if youtube:
    #         for y in youtube:
    #             sentence = sentence + y.title + " "
    #     if news:
    #         for n in news:
    #             sentence = sentence + n.title + " "

    #     if book:
    #         for b in book:
    #             sentence = sentence + b.title + " "

    #     if shopping:
    #         for s in shopping:
    #             sentence = sentence + s.title + " "

    #     like_sentence.append(sentence)
    #     data = {"like_sentence": like_sentence}
