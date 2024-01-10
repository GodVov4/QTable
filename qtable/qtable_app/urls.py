from django.urls import path

from .views import IndexView, QuotesListView, FavoritesListView, FavoriteSetView

app_name = 'qtable_app'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('quotes/<int:page>/', QuotesListView.as_view(), name='quotes'),
    path('favorites/', FavoritesListView.as_view(), name='favorites'),
    path('<int:pk>/', FavoriteSetView.as_view(), name='add_favorite'),
]
