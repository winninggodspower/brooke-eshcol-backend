from django.contrib import admin

# importing the use model
from .models import Member
from django.contrib.auth import get_user_model
User = get_user_model()


# Register your models here.
admin.site.register(User) #user's model
admin.site.register(Member) # Member model
