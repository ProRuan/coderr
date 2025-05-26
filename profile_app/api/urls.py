# Third-party suppliers
from django.urls import path

# Local imports
from .views import (
    BusinessProfileListView, CustomerProfileListView,
    ProfileDetailAPIView
)

urlpatterns = [
    path(
        '<int:pk>/',
        ProfileDetailAPIView.as_view(),
        name='profile-detail'
    ),
    path(
        'business/',
        BusinessProfileListView.as_view(),
        name='business-profiles'
    ),
    path(
        'customer/',
        CustomerProfileListView.as_view(),
        name='customer-profiles'
    ),
]
