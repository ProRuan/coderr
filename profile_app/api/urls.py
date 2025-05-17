# 1. Standard libraries

# 2. Third-party suppliers
from django.urls import path

# 3. Local imports
from .views import BusinessProfileListView, CustomerProfileListView

urlpatterns = [
    path('business/', BusinessProfileListView.as_view(),
         name='business-profiles'),
    path('customer/', CustomerProfileListView.as_view(),
         name='customer-profiles'),
]
