from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "nickname", "bio", "img")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("nickname", "password", "bio", "img")
