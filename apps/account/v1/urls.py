from django.urls import include, path

from apps.account.v1.apis.user_api import SignUpView

app_name = "account"

urlpatterns = [
    path("signup", SignUpView.as_view(), name="signup"),
]
