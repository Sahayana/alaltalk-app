from tkinter import E
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

# User 생성용 헬퍼 클래스
# User 생성에 필요한 행위 지정
# 장고 모든 모델은 Manager를 거쳐서 Queryset을 받음
class CustomUserManager(BaseUserManager):

    def _create_user(self, email, nickname, password, **extra_fields):
        
        if not email:
            raise ValueError('이메일 주소를 설정해주세요.')
        if not nickname:
            raise ValueError('닉네임을 설정해주세요.')
        
        email = self.normalize_email(email) # 중복 최소화를 위한 소문자로 정규화        
        user = self.model(email = email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # 일반 회원 생성
    def create_user(self, email, nickname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
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
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)    
    bio = models.CharField(max_length=150, blank=True)
    img = models.ImageField(default="https://sahayana-nts.s3.ap-northeast-2.amazonaws.com/style_pepe.png", null=True, blank=True, upload_to = "profile_images/")
    
    # Boolean field
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#django.contrib.auth.models.CustomUser
    USERNAME_FIELD = 'email'    # 이메일 로그인
    REQUIRED_FIELDS = ['nickname']   # REQUIRED_FIELDS: 필수적으로 받고 싶은 값

    # 위에서 정의한 Manager 지정
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    # is_admin이 True면 obj에 대한 권한을 가짐
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    

    