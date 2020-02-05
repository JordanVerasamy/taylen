from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('slack', views.slack, name="slack"),
    path('ping', views.ping, name="ping"),
    path('', views.emoji_tree, name="emoji_tree"),
]
