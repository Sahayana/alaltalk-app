from django.db import models
from django.utils.translation import gettext_lazy as _


class FriendRequestStatus(models.IntegerChoices):
    SENT = 0, _("SENT")
    ACCEPT = 1, _("ACCEPT")
    DECLINE = 2, _("DECLINE")


class FriendStatus(models.IntegerChoices):
    CONNECTED = 0, _("CONNECTED")
    DISCONNECTED = 1, _("DISCONNECTED")
