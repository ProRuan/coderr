# # 1. Standard libraries
# from datetime import datetime

# # 2. Third-party suppliers
# from django.contrib.auth.models import User
# from django.db import models
# from django.utils.timezone import now

# # 3. Local imports
# from auth_app.models import UserProfile


# class Profile(UserProfile):
#     """
#     Extended profile model for both customers and businesses.
#     Field 'type' defines whether profile is a 'customer' or 'business'.
#     """
#     username = models.CharField(max_length=150)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     file = models.ImageField(upload_to='profiles/', blank=True)
#     location = models.CharField(max_length=100, blank=True)
#     tel = models.CharField(max_length=20, blank=True)
#     description = models.TextField(blank=True)
#     working_hours = models.CharField(max_length=100, blank=True)
#     uploaded_at = models.DateTimeField(auto_now=True)  # auto_now_add=True?
#     # uploaded_at = models.DateTimeField(auto_now_add=True)
