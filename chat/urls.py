from django.urls import path

from chat import views

app_name = "chat"

urlpatterns = [
    # path("userlist/", views.get_user_list, name="userlist"),
    path("", views.show_chat_list, name="show_chat_list"),
    path("<int:id>/", views.create_chat_room, name="create_chat_room"),
    path("room/<int:room_id>/", views.create_chat_message, name="create_chat_message"),
    # path("loadmessage/", views.load_last_message, name="load_last_message"),
]
