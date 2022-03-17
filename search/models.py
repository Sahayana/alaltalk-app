from django.db import models

from accounts.models import CustomUser


# Create your models here.
class Youtube(models.Model):
    user = models.ForeignKey(CustomUser, related_name="youtube", on_delete=models.CASCADE)
    url = models.URLField(max_length=1000)


class News(models.Model):
    user = models.ForeignKey(CustomUser, related_name="news", on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    date = models.CharField(max_length=1000)
    company = models.CharField(max_length=1000)
    content = models.TextField()
    thumbnail = models.ImageField()
    link = models.URLField()


class Book(models.Model):
    user = models.ForeignKey(CustomUser, related_name="book", on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    date = models.CharField(max_length=1000)
    author = models.CharField(max_length=1000)
    company = models.CharField(max_length=1000)
    thumbnail = models.ImageField()
    link = models.URLField()


class Shopping(models.Model):
    user = models.ForeignKey(CustomUser, related_name="shopping", on_delete=models.CASCADE)
    price = models.CharField(max_length=1000)
    date = models.CharField(max_length=1000)
    thumbnail = models.ImageField()
    link = models.URLField()
