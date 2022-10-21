from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class User(AbstractUser):
    phone = models.IntegerField(null = True)

    def __str__(self):
        return self.username

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    conf_num = models.CharField(max_length=15, null=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email + " (" + ("not " if not self.confirmed else "") + "confirmed)"


class Member(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    email = models.EmailField(unique = True)
    phone =PhoneNumberField(unique = True, null = False, blank = False)
    city = models.CharField(max_length = 40)
    state = models.CharField(max_length = 40)
    zip_code = models.CharField(max_length = 20)

    def __str__(self):
        return self.first_name + ' ' + self.last_name