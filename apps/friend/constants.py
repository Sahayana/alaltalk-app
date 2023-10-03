from django.db import models


class FriendRequestStatus(models.IntegerChoices):
    SENT = 0, "SENT"
    ACCEPT = 1, "ACCEPT"
