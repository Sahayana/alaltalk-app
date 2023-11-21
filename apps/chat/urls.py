from django.urls import include, path

app_name = "chat"

urlpatterns = [
    path("v1/", include("apps.chat.apis.v1.urls", namespace="v1")),
]
