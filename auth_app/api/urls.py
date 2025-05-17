# 1. Standard libraries

# 2. Third-party suppliers
from django.urls import path

# 3. Local imports
from .views import LoginView, RegistrationView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
]
