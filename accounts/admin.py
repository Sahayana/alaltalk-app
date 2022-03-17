from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from accounts.forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
    UserChangeForm,
    UserCreationForm,
)
from accounts.models import CustomUser

# Register your models here.


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ["email", "nickname"]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
