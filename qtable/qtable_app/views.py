import httpx
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View, ListView

from .models import QuoteOfDay


class BaseQuoteView(View):
    url = None

    def get_response(self, page: int = None) -> dict | list:
        if page:
            self.url = f'{self.url}?page={page}'
        response = httpx.get(self.url)
        return response.json()


class IndexView(BaseQuoteView):
    template_name = 'qtable_app/index.html'
    url = 'https://api.quotable.io/quotes/random'

    def get(self, request: HttpRequest, page: int = None) -> HttpResponse:
        quote_of_day = QuoteOfDay.objects.filter(date__date=date.today()).first()
        if not quote_of_day:
            response = self.get_response()[0]
            quote_of_day = QuoteOfDay(quote=response.get('content'), author=response.get('author'))
            quote_of_day.save()
        content = {
            'title': 'Quote of the Day',
            'quote': quote_of_day,
            'favorites': request.user.favorites.all() if request.user.is_authenticated else None
        }
        return render(request, self.template_name, content)


class QuotesListView(BaseQuoteView):
    template_name = 'qtable_app/quotes_list.html'
    url = 'https://api.quotable.io/quotes'

    def get(self, request: HttpRequest, page: int = None) -> HttpResponse:
        context = {
            'title': 'Quotes List',
            'quotes': self.get_response(page),
            'favorites': request.user.favorites.all() if request.user.is_authenticated else None
        }
        return render(request, self.template_name, context)


class FavoritesListView(LoginRequiredMixin, ListView):
    template_name = 'qtable_app/favorites.html'
    url = 'https://api.quotable.io/quotes'
    paginate_by = 4

    def get_queryset(self) -> User:
        return self.request.user.favorites.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Favorites'
        context['favorites'] = self.request.user.favorites.all()
        return context


class FavoriteSetView(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        user = get_object_or_404(User, pk=request.user.pk)
        favorite = get_object_or_404(QuoteOfDay, pk=pk)
        if favorite in user.favorites.all():
            user.favorites.remove(favorite)
        else:
            user.favorites.add(favorite)
        user.save()
        next_url = request.GET.get('next', reverse('qtable_app:index'))
        return redirect(next_url)
