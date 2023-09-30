from django.urls import path

from apps.account.v1.apis import user_api

app_name = "account"

urlpatterns = [
    path("signup", user_api.SignUpView.as_view(), name="signup"),
    path(
        "signup/verification/<str:uidb64>/<str:token>",
        user_api.UserActivationView.as_view(),
        name="user_activation",
    ),
    path("login", user_api.LoginView.as_view(), name="login"),
]
