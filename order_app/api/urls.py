# 1. Standard libraries

# 2. Third-party suppliers
from django.urls import path

# 3. Local imports
from .views import OrderListCreateView

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order-list-create'),
]
