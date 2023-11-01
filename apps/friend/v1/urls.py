from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.friend.v1.apis.friend_api import FriendViewSet
from apps.friend.v1.apis.friend_request_api import FriendRequestViewSet

app_name = "friend"

router = DefaultRouter()
router.register("friend_request", FriendRequestViewSet, "friend_request")
router.register("friends", FriendViewSet, basename="friends")

urlpatterns = [
    path("", include(router.urls)),
]
