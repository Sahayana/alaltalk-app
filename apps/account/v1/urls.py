from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenBlacklistView

from apps.account.v1.apis import user_api
from apps.account.v1.apis.mypage_api import MyPageViewSet

app_name = "account"

router = DefaultRouter()
router.register("mypage", MyPageViewSet, "mypage")

urlpatterns = [
    path("", include(router.urls)),
    path("signup", user_api.SignUpView.as_view(), name="signup"),
    path(
        "signup/verification/<str:uidb64>/<str:token>",
        user_api.UserActivationView.as_view(),
        name="user_activation",
    ),
    path("login", user_api.LoginView.as_view(), name="login"),
    path(
        "login/temp",
        user_api.TemporaryPasswordView.as_view(),
        name="temporary_password",
    ),
    path("logout", TokenBlacklistView.as_view(), name="logout"),
]
