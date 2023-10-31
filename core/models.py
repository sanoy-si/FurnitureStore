from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
  email = models.EmailField(unique=True)
  phone_no = models.CharField(max_length=10)
  first_name = models.CharField(("first name"), max_length=150)
