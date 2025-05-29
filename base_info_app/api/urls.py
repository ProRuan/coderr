# Third-party suppliers
from django.urls import path

# Local imports
from .views import BaseInfoAPIView


urlpatterns = [
    path('', BaseInfoAPIView.as_view(), name='base-info'),
]
