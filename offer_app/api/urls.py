# 1. Standard libraries

# 2. Third-party suppliers
from django.urls import path

# 3. Local imports
from .views import OfferListCreateAPIView

urlpatterns = [
    path('', OfferListCreateAPIView.as_view(), name='offer-list-create'),
]
