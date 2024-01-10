"""
This module defines URL patterns related to the 'qtable_app' within the Django application.

URL Patterns:
    - '': Maps to the IndexView class, serving as the main landing page of the application.
    - 'quotes/<int:page>/': Maps to the QuotesListView class, displaying a paginated list of quotes from the external
        API.
    - 'favorites/': Maps to the FavoritesListView class, displaying a list of favorite quotes for the authenticated
        user.
    - '<int:pk>/': Maps to the FavoriteSetView class, allowing users to toggle the favorite status for a specific quote
        of the day.

Views:
    - IndexView: Represents the main landing page of the application, displaying the quote of the day.
    - QuotesListView: Displays a paginated list of quotes fetched from an external API.
    - FavoritesListView: Displays a list of favorite quotes for the authenticated user.
    - FavoriteSetView: Allows users to add or remove a specific quote from their favorites.

Usage:
    The URL configuration ensures that users can navigate to appropriate endpoints within the 'qtable_app', including
    viewing quotes, managing favorites, and toggling favorite statuses.
    Each URL pattern is associated with a specific view class, providing functionality tailored to the user's
    interaction with the application.

Note:
    The 'app_name' variable is set to 'qtable_app', ensuring that the URL patterns are namespaced under the 'qtable_app'
    application.
"""

from django.urls import path

from .views import FavoriteSetView, FavoritesListView, IndexView, QuotesListView

app_name = 'qtable_app'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('quotes/<int:page>/', QuotesListView.as_view(), name='quotes'),
    path('favorites/', FavoritesListView.as_view(), name='favorites'),
    path('<int:pk>/', FavoriteSetView.as_view(), name='add_favorite'),
]
