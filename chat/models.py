# from django.db import models
# from accounts.models import CustomUserManager
#
#
# class ChatRoom(models.Model):
#     class Meta:
#         db_table = "chat"
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     participant1 = models.ForeignKey(CustomUserManager, on_delete=models.CASCADE)
#     participant2 = models.ForeignKey(CustomUserManager, on_delete=models.CASCADE)
#
#
# class ChatMessage(models.Model):
#     class Meta:
#         db_table = "message"
#     chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
#     author = models.ForeignKey(CustomUserManager, on_delete=models.CASCADE)
#     message = models.CharField(max_length=256)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
