# Standard libraries
from datetime import timedelta

# Third-party suppliers
from django.db import models

# Local imports
from auth_app.models import CustomUser


class Order(models.Model):
    """
    Represents a customer's order against a business offer.
    """
    STATUS_CHOICES = (
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    )

    customer_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="orders_as_customer",
        verbose_name="customer",
    )
    business_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="orders_as_business",
        verbose_name="business",
    )
    title = models.CharField(max_length=255, blank=False, default='')
    revisions = models.IntegerField(default=-1)
    delivery_time_in_days = models.PositiveIntegerField(default=0)
    price = models.IntegerField(default=0)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=50)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='in_progress',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        """
        Get a string representing an order.
        """
        return f"Order #{self.id}: {self.title} ({self.status})"
