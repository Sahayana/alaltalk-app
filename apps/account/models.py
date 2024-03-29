from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from apps.account.constants import IMG_UPLOAD_TO
from apps.base_model import BaseModel
from apps.friend.models import Friend


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, nickname, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, nickname, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, nickname, password, **extra_fields)

    def create_superuser(self, email, nickname, password, **extra_fields):
        user = self.create_user(email=email, password=password, nickname=nickname)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    nickname = models.CharField(max_length=30)
    bio = models.CharField(max_length=150, blank=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    friends = models.ManyToManyField(
        "self",
        through="friend.Friend",
        through_fields=("user", "target_user"),
    )

    # Boolean field
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_recommend_on = models.BooleanField(default=True)
    is_like_public = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    # 위에서 정의한 Manager 지정
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserProfileImage(BaseModel):

    user = models.ForeignKey(
        CustomUser,
        null=True,
        on_delete=models.CASCADE,
        related_name="user_profile_imgs",
    )
    img = models.ImageField(
        upload_to=IMG_UPLOAD_TO,
    )


class UserLikeKeyWord(BaseModel):

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user_like_keywords"
    )
    keyword = models.CharField(max_length=100, default="", blank=True)
