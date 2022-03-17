from email.policy import default
from re import T

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    nickname = models.CharField(max_length=30, unique=True)
    bio = models.CharField(max_length=150, blank=True)
    img = models.ImageField(default="https://sahayana-nts.s3.ap-northeast-2.amazonaws.com/style_pepe.png", null=True, blank=True)

    def __str__(self):
        return self.email
