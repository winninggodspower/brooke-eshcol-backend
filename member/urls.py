from django.contrib import admin
from django.urls import re_path, path

from member import views

urlpatterns = [
    path('members', views.members.as_view(), name='members'),
]