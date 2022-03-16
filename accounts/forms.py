from django import forms
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from accounts.models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'nickname', 'password1', 'password2', 'bio', 'img')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'nickname', 'bio', 'img')
