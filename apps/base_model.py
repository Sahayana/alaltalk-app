from django.db import models


class BaseModel(models.Model):
    """
    모든 모델에 공통적으로 사용되는 기본 모델
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
