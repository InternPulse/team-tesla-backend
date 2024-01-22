'''
URL patterns for the user account API
'''
from django.urls import path
from account import views


app_name = 'account'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='sign_up'),
    path('signin/', views.SignInView.as_view(), name='sign_in'),
    path('refresh/token/', views.RefreshTokenView.as_view(), name='refresh_token'),
    path('profile/', views.ProfileView.as_view(), name='profile')
]
