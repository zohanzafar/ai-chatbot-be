from django.urls import path
from .views import UserRegistrationView, LogoutView, CustomObtainAuthToken

urlpatterns = [
    path('login/', CustomObtainAuthToken.as_view(), name='user_login'),
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
]
