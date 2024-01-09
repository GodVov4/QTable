from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import RegisterView, confirm_email

app_name = 'users'

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='users/login.html', authentication_form=AuthenticationForm,
                                     redirect_authenticated_user=True, extra_context={'title': 'Login'}), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('confirm_email/<int:pk>/', confirm_email, name='confirm_email'),
]
