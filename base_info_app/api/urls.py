from django.urls import path
from .views import BaseInfoAPIView

urlpatterns = [
    path('', BaseInfoAPIView.as_view(), name='base-info'),
]


# from django.urls import path
# from .views import BaseInfoView

# urlpatterns = [
#     path('', BaseInfoView.as_view(), name='base-info'),
# ]
