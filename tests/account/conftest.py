from io import BytesIO

import pytest
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from apps.account.constants import TEST_IMG_NAME
from apps.account.models import CustomUser


@pytest.fixture()
def create_user_data():
    """시리얼라이저 테스트를 위한 유저 데이터 생성 fixture 입니다."""

    def _create_user_data(user: CustomUser):

        data = {
            "email": user.email,
            "password": user.password,
            "nickname": user.nickname,
            "bio": user.bio,
        }

        return data

    return _create_user_data


@pytest.fixture()
def get_test_image():

    name = TEST_IMG_NAME
    ext = "png"
    size = (50, 50)
    color = (256, 0, 0)
    file = BytesIO()
    image = Image.new("RGBA", size=size, color=color)
    image.save(file, ext)
    file.seek(0)

    return File(file=file, name=name)


@pytest.fixture()
def simple_upload_image():
    image_data = BytesIO()
    image = Image.new("RGB", (100, 100), "white")
    image.save(image_data, format="png")
    image_data.seek(0)

    return SimpleUploadedFile("test.png", image_data.read(), content_type="image/png")
