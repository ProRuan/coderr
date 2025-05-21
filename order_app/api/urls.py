from django.urls import path
from order_app.api.views import OrderDetailAPIView, OrderListCreateAPIView

urlpatterns = [
    path('', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
]


# # 1. Standard libraries

# # 2. Third-party suppliers
# from django.urls import path

# # 3. Local imports
# from .views import OrderListCreateView, OrderDetailView

# # pk or id?!
# urlpatterns = [
#     path('', OrderListCreateView.as_view(), name='order-list-create'),
#     path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
# ]
