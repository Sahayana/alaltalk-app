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


# 현재 AWS S3 storage는 서버가 닫은 관계로 사용하지 않습니다.
# # # AWS S3 connection

# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"


# with open(os.path.join(BASE_DIR, "alaltalk/config/aws.json")) as f:
#     secret = json.loads(f.read())

# AWS_ACCESS_KEY_ID = secret["AWS"]["ACCESS_KEY_ID"]
# AWS_SECRET_ACCESS_KEY = secret["AWS"]["SECRET_ACCESS_KEY"]
# AWS_STORAGE_BUCKET_NAME = secret["AWS"]["STORAGE_BUCKET_NAME"]
# AWS_REGION = "ap-northeast-2"
# AWS_DEFAULT_ACL = "public-read"
# AWS_S3_CUSTOM_DOMAIN = "%s.s3.%s.amazonaws.com" % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)
