from django.urls import path

from .views import IndexView, QuotesListView

app_name = 'qtable_app'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('quotes/<int:page>/', QuotesListView.as_view(), name='quotes'),
]
