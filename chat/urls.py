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
    path("latestmessage/", views.latest_message, name="latest_message"),
    path("lastmessagelist/", views.last_message_list, name="last_message_list"),
    path("latestmessagenotconnected/", views.latest_message_not_connected, name="latest_message_not_connected"),
    path("getroomid/", views.get_room_id, name="get_room_id"),
    path("delete/<int:room_id>/", views.delete_chat_room, name="delete_chat_room"),
]
