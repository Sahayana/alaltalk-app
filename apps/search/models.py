from django.db import models

from apps.account.models import CustomUser
from apps.base_model import BaseModel


# Create your models here.
class Youtube(BaseModel):
    user = models.ForeignKey(
        CustomUser, related_name="youtube", on_delete=models.CASCADE
    )
    url = models.URLField(max_length=1000)
    title = models.CharField(max_length=1000, default="")
    views = models.CharField(max_length=1000, default="")


class News(BaseModel):
    user = models.ForeignKey(CustomUser, related_name="news", on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    date = models.CharField(max_length=1000)
    company = models.CharField(max_length=1000)
    content = models.TextField()
    thumbnail = models.URLField(max_length=1000, default="")
    link = models.URLField(max_length=1000)


class Book(BaseModel):
    user = models.ForeignKey(CustomUser, related_name="book", on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    price = models.CharField(max_length=1000)
    author = models.CharField(max_length=1000)
    company = models.CharField(max_length=1000)
    thumbnail = models.URLField(max_length=1000, default="")
    link = models.URLField()
    series = models.CharField(max_length=1000, default="")


class Shopping(BaseModel):
    user = models.ForeignKey(
        CustomUser, related_name="shopping", on_delete=models.CASCADE
    )
    price = models.CharField(max_length=1000)
    thumbnail = models.ImageField(max_length=1000)
    link = models.URLField(max_length=1000)
    title = models.CharField(max_length=1000)
