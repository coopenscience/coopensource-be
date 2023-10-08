from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    bio = models.CharField(max_length=2048, blank=True, null=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

