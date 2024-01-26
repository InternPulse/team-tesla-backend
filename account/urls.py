'''
URL patterns for the user account API
'''
from django.urls import path
from account import views


app_name = 'account'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='sign_up'),
    path('signin/', views.SignInView.as_view(), name='sign_in'),
    path('reset/password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('change/password/', views.ChangePasswordView.as_view(), name='password_reset'),
    path('refresh/token/', views.RefreshTokenView.as_view(), name='refresh_token'),
    path('profile/', views.ProfileView.as_view(), name='profile')
]
