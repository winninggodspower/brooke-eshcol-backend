from email.policy import default
import secrets
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

class Payment(models.Model):
    amount = models.PositiveIntegerField(default = 20_000)
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f"Payment: {self.amount}"

    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)

            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self) -> int:
        return self.amount * 100


