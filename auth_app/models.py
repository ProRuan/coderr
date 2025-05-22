# 1. Standard libraries

# 2. Third-party suppliers
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models

# 3. Local imports

# rename?!


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('business', 'Business'),
    )
    type = models.CharField(max_length=10, choices=USER_TYPES)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    file = models.ImageField(upload_to='profiles/', blank=True)
    location = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # auto_now_add=True?
    created_at = models.DateTimeField(auto_now_add=True)  # auto_now_add=True?
