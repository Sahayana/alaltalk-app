from django.urls import path

from chat import views

app_name = "chat"

urlpatterns = [
    path("", views.show_chat_list, name="show_chat_list"),
    path("<int:id>/", views.create_chat_room, name="create_chat_room"),
    path("room/<int:room_id>/", views.post_data_to_chat_room, name="post_data_to_chat_room"),
    path("chatlog/", views.chat_log_send, name="chat_log_send"),
]
