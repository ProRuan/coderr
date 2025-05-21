# 1. Standard libraries

# 2. Third-party suppliers
from django.db import models
# from django.contrib.auth.models import User

# 3. Local imports
from auth_app.models import CustomUser


class Review(models.Model):
    business_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="reviews_received"
    )
    reviewer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="reviews_written"
    )
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business_user', 'reviewer')
