import secrets
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .Paystack import PayStack


# Create your models here.

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


    def amount_value(self) -> int:
        return self.amount * 100

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()


        return self.verified


class Member(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    email = models.EmailField(unique = True)
    phone =PhoneNumberField(unique = True, null = False, blank = False)
    city = models.CharField(max_length = 40)
    state = models.CharField(max_length = 40)
    zip_code = models.CharField(max_length = 20)
    payment = models.ForeignKey(Payment, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

