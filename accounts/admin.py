from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import CustomUser

# Register your models here.

# https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#a-full-example

class CustomUserAdmin(UserAdmin):   
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'nickname', 'date_joined','is_admin')
    search_fields = ('email', 'nickname')
    readonly_fields = ('id', 'date_joined', 'last_login')

    # username을 쓰지 않기 때문에 email ordering으로 override
    ordering = ('email',)

    # UserAdmin fieldsets override: 완전히 새로운 User모델을 만들었기 때문에 fieldsets override 안하면 admin페이지에서 오류
    fieldsets = (
        (None, {'fields': ('id', 'email', 'password')}),
        ('Personal info', {'fields': ('nickname', 'bio', 'img')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superuser')}),
        ('Date', {'fields': ('date_joined', 'last_login')})
    )

    # admin 페이지에서 사용자 추가할때 입력폼
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'password1', 'password2', 'bio', 'img')
            }
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)