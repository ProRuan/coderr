"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Third-party suppliers
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Local imports
from offer_app.api.views import OfferDetailRetrieveAPIView
from order_app.api.views import (
    CompletedOrderCountAPIView, OpenOrderCountAPIView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('auth_app.api.urls')),
    path('api/profile/', include('profile_app.api.urls')),
    path('api/profiles/', include('profile_app.api.urls')),
    path('api/offers/', include('offer_app.api.urls')),
    path('api/offerdetails/<int:pk>/', OfferDetailRetrieveAPIView.as_view()),
    path('api/orders/', include('order_app.api.urls')),
    path(
        'api/order-count/<int:business_user_id>/',
        OpenOrderCountAPIView.as_view(),
        name='order-count'
    ),
    path(
        'api/completed-order-count/<int:business_user_id>/',
        CompletedOrderCountAPIView.as_view(),
        name='completed-order-count'
    ),
    path('api/reviews/', include('review_app.api.urls')),
    path('api/base-info/', include('base_info_app.api.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
