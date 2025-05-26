# Third-party suppliers
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Local imports
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin registration for CustomUser.
    """
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Info', {'fields': ('type',)}),
    )
    list_display = ('username', 'email', 'type', 'is_staff')
    ordering = ('username',)
