from enum import Enum

import jwt
from accounts.models import CustomUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import JsonResponse
from django.shortcuts import redirect
from six import text_type

from alaltalk.settings import SECRET_KEY


class AccountsVerifyTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.id) + text_type(timestamp)


accounts_verify_token = AccountsVerifyTokenGenerator()


class LoginConfirm:
    def __init__(self, func):
        self.func = func

    def __call__(self, request, *args, **kwargs):

        try:
            token = request.COOKIES["Authorization"]
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = CustomUser.objects.get(email=payload["email"])
            request.user = user
            return self.func(request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"msg": "EXPIRED_TOKEN"}, status=401)

        except (jwt.DecodeError, CustomUser.DoesNotExist):
            return JsonResponse({"msg": "INVALID_USER"}, status=401)

        except KeyError:
            return redirect("accounts:login")


class FriendType(Enum):
    is_friend = 0
    is_self = 1
    is_not_friend = 2
