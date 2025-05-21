# 1. Standard libraries
from datetime import timedelta

# 2. Third-party suppliers
from django.db import models
# from django.contrib.auth.models import User

# 3. Local imports
from auth_app.models import CustomUser
# none needed here


class Offer(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="offers")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='offers/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OfferDetail(models.Model):
    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    features = models.JSONField(default=None)
    offer_type = models.CharField(max_length=50, default=None)  # None or ''?


# # 1. Standard libraries

# # 2. Third-party suppliers
# from django.db import models
# from django.contrib.auth.models import User

# # 3. Local imports


# class Offer(models.Model):
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="offers"
#     )
#     title = models.CharField(max_length=255)
#     image = models.ImageField(upload_to='offers/', null=True, blank=True)
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     @property
#     def min_price(self):
#         return self.details.aggregate(models.Min('price'))['price__min']

#     @property
#     def min_delivery_time(self):
#         return self.details.aggregate(models.Min('delivery_time_in_days'))['delivery_time_in_days__min']


# class OfferDetail(models.Model):
#     offer = models.ForeignKey(
#         Offer, on_delete=models.CASCADE, related_name="details"
#     )
#     title = models.CharField(max_length=100)
#     revisions = models.IntegerField()
#     delivery_time_in_days = models.IntegerField()
#     price = models.FloatField()
#     features = models.JSONField()
#     offer_type = models.CharField(max_length=50)
