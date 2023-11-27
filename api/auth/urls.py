from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('password/', views.PassworUpdatedView.as_view(), name='password-update'),
    path('email/duplicate/', views.EmailDuplicateView.as_view(), name='email-duplicate')
]
