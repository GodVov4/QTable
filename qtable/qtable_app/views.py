import httpx
from datetime import date
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.generic import View

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
        return render(request, self.template_name, {'quote': quote_of_day, 'title': 'Quote of the Day'})


class QuotesListView(BaseQuoteView):
    template_name = 'qtable_app/quotes_list.html'
    url = 'https://api.quotable.io/quotes'

    def get(self, request: HttpRequest, page: int = None) -> HttpResponse:
        return render(request, self.template_name, {'quotes': self.get_response(page), 'title': 'Quotes List'})
