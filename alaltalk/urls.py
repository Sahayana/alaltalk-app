"""alaltalk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from ninja import NinjaAPI

from search.apis.v1.like_cancel_router import router as like_cancel_router
from search.apis.v1.like_router import router as like_router
from search.apis.v1.search_router import router as search_router
from chat.apis.v1.chat_room_router import router as chat_room_router

from . import views

api = NinjaAPI()
api.add_router("/search/", search_router)
api.add_router("/like/", like_router)
api.add_router("/like_cancel/", like_cancel_router)
api.add_router('/chat_room/', chat_room_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.landing_home, name="landing_page"),
    path("accounts/", include("accounts.urls")),
    path("chat/", include("chat.urls")),
    path("api/", api.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
