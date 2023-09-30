import os

from alaltalk.enviorment import get_secret
from alaltalk.settings.base import *
from alaltalk.settings.base import SIMPLE_JWT

get_secret(env="dev")

SECRET_KEY = os.environ["SECRET_KEY"]

SIMPLE_JWT.update({"SIGNING_KEY": SECRET_KEY})

# DB connection
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ["MYSQL_DB_NAME"],
        "USER": os.environ["MYSQL_DB_USERNAME"],
        "PASSWORD": os.environ["MYSQL_DB_PASSWORD"],
        "PORT": os.environ["MYSQL_DB_PORT"],
        "HOST": os.environ["MYSQL_DB_HOST"],
    }
}


# Email backend
EMAIL_BACKEND = os.environ["EMAIL_BACKEND"]
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_PORT = os.environ["EMAIL_PORT"]
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_USE_TLS = os.environ["EMAIL_USE_TLS"]
EMAIL_USE_SSL = os.environ["EMAIL_USE_SSL"]

# Test 환경에서 Celery task 항상 locally blocking 하도록 동작
CELERY_TASK_ALWAYS_EAGER = True
