from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
     
    phone = models.IntegerField(null = True)
    email_verified = models.BooleanField(default = False)

    def __str__(self):
        return self.username