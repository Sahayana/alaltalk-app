import pytest

from alaltalk.settings.base import CELERY_BROKER_URL, CELERY_RESULT_BACKEND


@pytest.fixture(scope="session")
def celery_config():
    return {"broker_url": CELERY_BROKER_URL, "result_backend": CELERY_RESULT_BACKEND}
