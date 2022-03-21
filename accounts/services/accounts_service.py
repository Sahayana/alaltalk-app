from django.contrib.auth import get_user_model


def create_user(email, nickname, password, bio, img):
    if img:
        user = get_user_model().objects.create_user(email=email, nickname=nickname, password=password, bio=bio, img=img)
    user = get_user_model().objects.create_user(email=email, nickname=nickname, password=password, bio=bio)
    return user
