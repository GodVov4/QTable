from django.contrib import admin
from django.urls import path, include
from django_email_verification import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('qtable_app.urls')),
    path('users/', include('users.urls')),
    path('email/', include(urls)),
]
