from rest_framework import generics, permissions, renderers, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.account.constants import EMAIL_DUPLICATION_MESSAGE
from apps.account.models import CustomUser
from apps.account.services.user_selector import UserSelector
from apps.account.services.user_service import UserService
from apps.account.v1.serializers.user_serializer import (
    UserCreateSerializer,
    UserLikeKeywordSerilaizer,
    UserReadSerializer,
)


class SignUpView(generics.ListCreateAPIView):

    permission_classes = [permissions.AllowAny]
    serializer_class = UserCreateSerializer

    def get_renderers(self):
        if self.request.method == "GET":
            renderer_classes = [renderers.TemplateHTMLRenderer]
        else:
            renderer_classes = [renderers.JSONRenderer]
        return [renderer() for renderer in renderer_classes]

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        """
        회원가입 페이지를 렌더링합니다.
        """
        return Response(template_name="account/signup.html", status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """ "
        회원가입을 통해 유저를 생성합니다.
        """
        request_data = {
            "email": request.data.get("email"),
            "nickname": request.data.get("nickname"),
            "password": request.data.get("password"),
            "bio": request.data.get("bio"),
            "img": request.data.get("img", None),
        }

        is_present = UserSelector.check_email_duplication(email=request_data["email"])

        if is_present:
            return Response(
                data={"msg": EMAIL_DUPLICATION_MESSAGE},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request_data)

        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            user = UserService.create_single_user(
                email=validated_data["email"],
                nickname=validated_data["nickname"],
                bio=validated_data["bio"],
                password=validated_data["password"],
                img=validated_data.get("img", None),
            )

            data = {"msg": "sent", "user": UserReadSerializer(instance=user).data}

            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(
            data=serializer.error_messages, status=status.HTTP_400_BAD_REQUEST
        )


class UserActivationView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        uidb64 = kwargs.get("uidb64", None)
        token = kwargs.get("token", None)

        user = UserService.verified_email_activation(uidb64=uidb64, token=token)

        if not user:
            return Response(
                data={"msg": "not_activated"}, status=status.HTTP_400_BAD_REQUEST
            )

        data = {
            "msg": "activated",
            "user": UserReadSerializer(instance=user).data,
        }

        return Response(data=data, status=status.HTTP_202_ACCEPTED)


class LoginView(TokenObtainPairView):

    permission_classes = [permissions.AllowAny]

    def get_renderers(self):
        if self.request.method == "GET":
            renderer_classes = [renderers.TemplateHTMLRenderer]
        else:
            renderer_classes = [renderers.JSONRenderer]
        return [renderer() for renderer in renderer_classes]

    def get(self, request, *args, **kwargs):
        """
        로그인 페이지를 렌더링합니다.
        """
        return Response(template_name="account/login.html", status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        이메일, 패스워드로 로그인하여 access token을 반환합니다.
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(data=serializer.validated_data, status=status.HTTP_200_OK)


# TODO: MyPage 작업에 추가
class LikePublicSettingView(views.APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        유저의 좋아요 컨텐츠 노출을 설정합니다.

        param
        -----
        user_id
        value = "ON" | "OFF"
        """
        user_id = request.user.id
        value = request.data.get("value", "ON")

        user = UserService.like_public_setting(user_id=user_id, value=value)

        data = {"result": "success", "user": UserReadSerializer(instance=user).data}

        return Response(data=data, status=status.HTTP_200_OK)


# TODO:친구 관련 API 개발에 추가
class UserLikeKeywordSaveView(views.APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        유저의 관심 키워드를 저장합니다.

        param
        -----
        user_id
        keyword
        """
        user_id = request.user.id
        keywword = request.data.get("keyword", "")

        liked_keyword = UserService.save_like_keyword(user_id=user_id, keyword=keywword)

        data = {
            "result": "success",
            "keyword": UserLikeKeywordSerilaizer(instance=liked_keyword).data,
        }
        return Response(data=data, status=status.HTTP_200_OK)
