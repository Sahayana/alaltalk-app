from django.urls import path

from chat import views

app_name = "chat"

urlpatterns = [
    path("", views.show_chat_list, name="show_chat_list"),
    path("<int:id>/", views.create_chat_room, name="create_chat_room"),
    path("room/<int:room_id>/", views.post_data_to_chat_room, name="post_data_to_chat_room"),
    path("chatlog/", views.chat_log_send, name="chat_log_send"),
    path("morelist/", views.more_list, name="more_list"),
    path("messageloader/", views.message_loader, name="massage_loader"),
]
