from django.db import models

from accounts.models import CustomUser


class ChatRoom(models.Model):
    class Meta:
        db_table = "chat"

    created_at = models.DateTimeField(auto_now_add=True)
    participant1 = models.CharField(max_length=256)
    participant2 = models.CharField(max_length=256)


class ChatMessage(models.Model):
    class Meta:
        db_table = "message"

    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author

    def last_10_messages():
        return ChatMessage.objects.order_by("-created_at").all()[:10]
