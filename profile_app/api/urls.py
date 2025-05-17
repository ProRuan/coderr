# 1. Standard libraries

# 2. Third-party suppliers
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 3. Local imports
from .views import BusinessProfileListView, CustomerProfileListView, ProfileViewSet

router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('business/', BusinessProfileListView.as_view(),
         name='business-profiles'),
    path('customer/', CustomerProfileListView.as_view(),
         name='customer-profiles'),
]


# # 1. Standard libraries

# # 2. Third-party suppliers
# from django.urls import path

# # 3. Local imports
# from .views import BusinessProfileListView, CustomerProfileListView, ProfileDetailView, ProfileUpdateView

# router = DefaultRouter()
# router.register(r'profile', ProfileViewSet, basename='profile')

# urlpatterns = [
#     path('<int:pk>/', ProfileUpdateView.as_view(), name='profile-update'),
#     path('<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
#     path('business/', BusinessProfileListView.as_view(),
#          name='business-profiles'),
#     path('customer/', CustomerProfileListView.as_view(),
#          name='customer-profiles'),
# ]
