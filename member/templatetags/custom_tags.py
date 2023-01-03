from django import template
from django.conf import settings

register = template.Library()

ALLOWABLE_VALUES = ("PAYSTACK_PUBLIC_KEY", "BECOME_MEMBER_PRICE")

def get_setting(name):
    if name in ALLOWABLE_VALUES:
        return getattr(settings, name, "")
    return

register.filter('get_setting', get_setting)