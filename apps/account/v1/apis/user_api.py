from rest_framework import generics, permissions, renderers, status, views
from rest_framework.response import Response

from apps.account.constants import EMAIL_DUPLICATION_MESSAGE
from apps.account.models import CustomUser
from apps.account.services.user_selector import UserSelector
from apps.account.services.user_service import UserService
from apps.account.v1.serializers.user_serializer import (
    UserCreateSerializer,
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
        self.renderer_classes = [renderers.TemplateHTMLRenderer]
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
