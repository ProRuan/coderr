# Third party-suppliers
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Represents a custom user including profile-specific fields.
    """
    USER_TYPES = (
        ('customer', 'Customer'),
        ('business', 'Business'),
    )

    type = models.CharField(
        max_length=10,
        choices=USER_TYPES,
        blank=False,
        default='customer',
        verbose_name='User Type'
    )
    file = models.ImageField(
        upload_to='profiles/',
        blank=True,
        default=None,
        verbose_name='Profile Picture'
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Location'
    )
    tel = models.CharField(
        max_length=20,
        blank=True,
        default='',
        verbose_name='Telephone'
    )
    description = models.TextField(
        blank=True,
        default='',
        verbose_name='Description'
    )
    working_hours = models.CharField(
        max_length=100,
        blank=False,
        default='16-20',
        verbose_name='Working Hours'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    uploaded_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        """
        Get a string representing a custom user.
        """
        return self.username
