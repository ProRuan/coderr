# 1. Standard libraries

# 2. Third-party suppliers
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models

# 3. Local imports
from auth_app.models import UserProfile


class Profile(UserProfile):
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    file = models.ImageField(upload_to='profiles/', blank=True)
    location = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=100, blank=True)


# rename profile to BusinessProfile or only one profile!?!


class CustomerProfile(UserProfile):
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    file = models.ImageField(upload_to='profiles/', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


# # 1. Standard libraries

# # 2. Third-party suppliers
# from django.contrib.auth.models import User
# from django.db import models

# # 3. Local imports


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
#     username = models.CharField(max_length=150)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     file = models.ImageField(upload_to='profiles/', blank=True)
#     location = models.CharField(max_length=100, blank=True)
#     tel = models.CharField(max_length=20, blank=True)
#     description = models.TextField(blank=True)
#     working_hours = models.CharField(max_length=50, blank=True)
#     type = models.CharField(max_length=10, choices=[('customer', 'Customer'), ('business', 'Business')])
#     created_at = models.DateTimeField(auto_now_add=True)
