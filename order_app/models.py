# 1. Standard libraries
from datetime import timedelta

# 2. Third-party suppliers
from django.db import models
# from django.contrib.auth.models import User

# 3. Local imports
from auth_app.models import CustomUser
from offer_app.models import OfferDetail


class Order(models.Model):
    customer_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="orders_as_customer")
    business_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="orders_as_business")
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="in_progress")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def estimated_delivery_date(self):
        return self.created_at + timedelta(days=self.delivery_time_in_days)
