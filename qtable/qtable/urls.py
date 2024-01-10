"""
This module defines the URL patterns for routing within the Django application, including admin, app-specific views,
user-related views, and email verification.

URL Patterns:
    - 'admin/': Maps to the Django admin site for administrative tasks and management.
    - '': Includes URL patterns from the 'qtable_app' application for handling specific app-related views.
    - 'users/': Includes URL patterns from the 'users' application for managing user-related views such as registration,
        login, and logout.
    - 'email/': Includes URL patterns for email verification using the django_email_verification package.

Usage:
    The URL configuration ensures proper routing within the Django application, allowing users to access various
    functionalities such as administrative tasks, app-specific views, user management, and email verification.
    Each URL pattern is associated with a specific application or functionality, ensuring a structured and organized
    routing system for the application.

Note:
    The use of the 'include' function allows for modular URL configuration by including URL patterns from other Django
    applications or packages, facilitating maintainability and scalability.
"""
from django.contrib import admin
from django.urls import include, path
from django_email_verification import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('qtable_app.urls')),
    path('users/', include('users.urls')),
    path('email/', include(urls)),
]
