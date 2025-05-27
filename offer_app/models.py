# Third-party suppliers
from django.db import models

# Local imports
from auth_app.models import CustomUser


class Offer(models.Model):
    """
    Represents an offer created by a business user.
    """
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="offers"
    )
    title = models.CharField(max_length=100, blank=False, default='')
    image = models.ImageField(upload_to='offers/', null=True, blank=True)
    description = models.TextField(max_length=500, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Offer"
        verbose_name_plural = "Offers"

    def __str__(self):
        """
        Get a string representing an offer.
        """
        return f"{self.title} by {self.user.username}"


class OfferDetail(models.Model):
    """
    Represents a pricing and feature tier of an offer.
    """
    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name="details"
    )
    title = models.CharField(max_length=100, blank=False, default='')
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=50, default='Basic')

    class Meta:
        verbose_name = "Offer Detail"
        verbose_name_plural = "Offer Details"
        ordering = ['price']

    def __str__(self):
        """
        Get a string representing an offer detail.
        """
        return f"{self.offer_type.title()} - {self.title} (${self.price})"
