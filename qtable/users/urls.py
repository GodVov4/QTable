"""
This module defines URL patterns related to user authentication and registration within the application.

URL Patterns:
    - 'signup/': Maps to the RegisterView class to handle user registration.
    - 'login/': Maps to the LoginView class for user authentication. It uses a custom template and form for login,
        and handles redirecting authenticated users to the appropriate page.
    - 'logout/': Maps to the LogoutView class to handle user logout functionality.
    - 'confirm_email/<int:pk>/': Maps to the confirm_email view function to confirm a user's email address,
        using a specific primary key.

Views and Forms:
    - RegisterView: Handles user registration, allowing new users to create accounts.
    - LoginView: Manages user authentication, providing a custom login template and form.
    - LogoutView: Implements user logout functionality to end user sessions.
    - confirm_email: A view function that confirms a user's email address by accepting a primary key as an argument.

Usage:
    The URL configuration ensures that users can navigate to appropriate endpoints for user registration, login, logout,
    and email confirmation.
    The provided views and forms manage user authentication processes, allowing users to interact securely with the
    application.
    The 'extra_context' parameter in the LoginView is utilized to provide additional context data, such as the title for
    the login page.

Note:
    The 'app_name' variable is set to 'users', ensuring that the URL patterns are namespaced under the 'users'
    application.
"""
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import RegisterView, confirm_email

app_name = 'users'

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path(
        'login/',
        LoginView.as_view(
            template_name='users/login.html',
            authentication_form=AuthenticationForm,
            redirect_authenticated_user=True,
            extra_context={'title': 'Login'},
        ), name='login',
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('confirm_email/<int:pk>/', confirm_email, name='confirm_email'),
]
