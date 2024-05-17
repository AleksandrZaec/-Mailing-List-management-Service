from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, VerifyEmailView, ProfileView, UserListView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify_email/<str:uid>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('users_list/', UserListView.as_view(), name='users_list'),
]