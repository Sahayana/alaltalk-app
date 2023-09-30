import os

from alaltalk.enviorment import get_secret
from alaltalk.settings.dev import *
from alaltalk.settings.dev import SIMPLE_JWT

get_secret(env="prod")

DEBUG = bool(os.environ["DEBUG"])

SECRET_KEY = os.environ["SECRET_KEY"]

SIMPLE_JWT.update({"SIGNING_KEY": SECRET_KEY})

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


# Email backend configuration
EMAIL_BACKEND = os.environ["EMAIL_BACKEND"]
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_PORT = os.environ["EMAIL_PORT"]
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_USE_TLS = os.environ["EMAIL_USE_TLS"]
EMAIL_USE_SSL = os.environ["EMAIL_USE_SSL"]
