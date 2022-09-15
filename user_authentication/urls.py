from django.contrib import admin
from django.urls import re_path, path

from user_authentication import views

urlpatterns = [
    path('',  views.home, name='home'),
    path('home',  views.home, name='home'),

    path('login', views.login_user, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_user, name='logout'),
    path('services', views.services, name='services'),
     path('newsub/', views.newSubscriber, name='newsub'),
    
    path("password_reset", views.password_reset_request, name="password_reset")
]