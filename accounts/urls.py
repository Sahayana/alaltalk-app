from django.urls import path

from accounts import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("signup/check/", views.duplicated_check, name="duplicated_check"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("login/temp/", views.temporary_password, name="temporary_password"),
    path("friends/", views.friend_list, name="friend_list"),
    path("mypage/", views.mypage, name="mypage"),
    path("mypage/modify/", views.profile_change, name="profile_change"),
    path("friends/search/", views.search_friend, name="search_friend"),
    path("friends/request/<int:receiver_id>/", views.send_request, name="send_request"),
    path("friends/accept/<int:request_id>/", views.accept_request, name="accept_request"),
]
