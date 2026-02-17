from django.urls import path
from .views import RegistrationView, LoginView, UserDeleteView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/<int:user_id>/', UserDeleteView.as_view(), name='user-delete'),
]