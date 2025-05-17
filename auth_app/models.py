# 1. Standard libraries

# 2. Third-party suppliers
from django.contrib.auth.models import User
from django.db import models

# 3. Local imports


# rename?!
class UserProfile(models.Model):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('business', 'Business'),
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    type = models.CharField(max_length=10, choices=USER_TYPES)
