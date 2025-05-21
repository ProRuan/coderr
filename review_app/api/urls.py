from django.urls import path
from review_app.api.views import ReviewListCreateAPIView, ReviewDetailAPIView

urlpatterns = [
    path('', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),
]


# from django.urls import path
# from .views import ReviewDetailView, ReviewListCreateView

# urlpatterns = [
#     path('', ReviewListCreateView.as_view(), name='review-list-create'),
#     path('<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
# ]
