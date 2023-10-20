from django.db import IntegrityError
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from apps.friend.models import FriendRequest
from apps.friend.services.friend_service import FriendService
from apps.friend.v1.serializers.friend_serializer import FriendRequestSerializer
from apps.pagination import CommonPagination


class FriendRequestViewSet(viewsets.ModelViewSet):

    queryset = FriendRequest.objects.select_related("user", "target_user").all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendRequestSerializer
    pagination_class = CommonPagination

    def create(self, request, *args, **kwargs):
        """친구 요청을 전송합니다."""
        user_id = request.data.get("user_id")
        target_user_id = request.data.get("target_user_id")

        try:
            friend_request = FriendService.send_friend_request(
                user_id=user_id, target_user_id=target_user_id
            )
            serializer = self.get_serializer(friend_request)
            data = {"msg": "sent", "data": serializer.data}
            return Response(data=data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            data = {"msg": "already"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk: int):
        """친구 요청을 승낙합니다."""

        try:
            friend_request = FriendService.accept_friend_request(
                target_user_id=request.user.id, request_id=pk
            )
            serializer = self.get_serializer(friend_request)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            raise exception

    def destroy(self, request, pk: int):
        """친구 요청을 거절합니다."""

        try:
            FriendService.decline_friend_request(
                target_user_id=request.user.id, request_id=pk
            )
            friend_request = FriendRequest.objects.filter(id=pk).get()
            serializer = self.get_serializer(friend_request)
            data = {"msg": "declined", "data": serializer.data}
        except Exception as exception:
            raise exception
        return Response(data=data, status=status.HTTP_200_OK)
