from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
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