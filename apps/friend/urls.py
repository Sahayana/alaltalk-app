from django.urls import include, path

app_name = "friend"

urlpatterns = [
    path("v1/", include("apps.friend.v1.urls", namespace="v1")),
]
