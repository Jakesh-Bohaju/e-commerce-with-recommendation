from django.contrib.auth.models import AbstractUser
from django.db import models


class EcommerceUser(AbstractUser):
    is_vendor = models.BooleanField(default=False)
