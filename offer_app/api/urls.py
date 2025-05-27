# Third-party suppliers
from django.urls import path

# Local imports
from .views import OfferDetailView, OfferListCreateAPIView


urlpatterns = [
    path('', OfferListCreateAPIView.as_view(), name='offer-list-create'),
    path('<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
]
