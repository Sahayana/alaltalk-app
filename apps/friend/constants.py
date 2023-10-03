from django.db import models


class FriendRequestStatus(models.IntegerChoices):
    SENT = 0, "SENT"
    ACCEPT = 1, "ACCEPT"
    DECLINE = 2, "DECLINE"


class FriendStatus(models.IntegerChoices):
    CONNECTED = 0, "CONNECTED"
    DISCONNECTED = 1, "DISCONNECTED"
