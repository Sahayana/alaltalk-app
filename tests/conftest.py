import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from alaltalk.settings.base import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from apps.account.models import CustomUser
from apps.account.utils import random_string_generator
from tests.account.factories import UserFactory


@pytest.fixture(scope="session")
def celery_config():
    return {"broker_url": CELERY_BROKER_URL, "result_backend": CELERY_RESULT_BACKEND}
