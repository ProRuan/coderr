# Third-party suppliers
from django.db import models

# Local imports
from auth_app.models import CustomUser


class Review(models.Model):
    """
    Represents a customer´s review of a business user.
    """
    business_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="reviews_received"
    )
    reviewer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="reviews_written"
    )
    rating = models.IntegerField(default=0)
    description = models.TextField(max_length=500, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business_user', 'reviewer')

    def __str__(self):
        """
        Get a string representing a review.
        """
        return f"{self.business_user} {self.rating} by {self.reviewer}"
