# Third-party suppliers
from django.urls import path

# Local imports
from order_app.api.views import OrderDetailAPIView, OrderListCreateAPIView

urlpatterns = [
    path('', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
]
