from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.friend.v1.apis.friend_request_api import FriendRequestViewSet

app_name = "friend"

router = DefaultRouter()
router.register("friend_request", FriendRequestViewSet, "friend_request")

urlpatterns = [
    path("", include(router.urls)),
]
