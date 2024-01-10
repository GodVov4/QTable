"""
This module contains Django views related to handling quotes from an external API and managing user favorites.

Classes:
    - BaseQuoteView: A base view class to fetch quotes from a specified URL.
    - IndexView: A view class to display the quote of the day.
    - QuotesListView: A view class to display a list of quotes from the external API.
    - FavoritesListView: A view class to display a list of favorite quotes for the authenticated user.
    - FavoriteSetView: A view class to toggle the favorite status for a specific quote of the day.

Attributes:
    - url: The URL from which quotes are fetched, specified in each respective view class.

Methods:
    - get_response(): Fetches a response from the specified URL, optionally paginating through results.
    - IndexView.get(): Renders the template for the quote of the day, fetching it from an API if not available.
    - QuotesListView.get(): Renders a template displaying a list of quotes from an external API.
    - FavoritesListView.get_queryset(): Returns a queryset of favorite quotes for the authenticated user.
    - FavoritesListView.get_context_data(): Provides context data for rendering the favorites list view.
    - FavoriteSetView.get(): Toggles the favorite status of a specific quote for the authenticated user.

Usage:
    This module provides the necessary views to display quotes, manage user favorites, and toggle favorite status.
    It integrates with an external API ('https://api.quotable.io/') to fetch quotes and allows users to mark quotes as
    favorites.
    The views are designed to handle user authentication, providing a personalized experience based on user preferences.

Note:
    The 'LoginRequiredMixin' is used to ensure that only authenticated users can access certain views, such as managing
    favorites.
"""

from datetime import date

import httpx
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView, View

from .models import QuoteOfDay


class BaseQuoteView(View):
    """A base view class for retrieving quotes from a given URL."""

    url = None

    def get_response(self, page: int = None) -> dict | list:
        """
        Retrieve a response from the given URL.

        :param page: The page number to retrieve. Defaults to None.
        :type page: int, optional

        :return: The JSON response from the URL.
        :rtype: dict | list
        """
        if page:
            self.url = f'{self.url}?page={page}'
        response = httpx.get(self.url)
        return response.json()


class IndexView(BaseQuoteView):
    """A view class for displaying the quote of the day."""

    template_name = 'qtable_app/index.html'
    url = 'https://api.quotable.io/quotes/random'

    def get(self, request: HttpRequest, page: int = None) -> HttpResponse:
        """
        Retrieve the quote of the day and renders it along with additional context data.

        :param request: The HTTP request object.
        :type request: HttpRequest
        :param page: The page number.
        :type page: int, optional
        :return: The HTTP response containing the rendered template.
        :rtype: HttpResponse
        """
        quote_of_day = QuoteOfDay.objects.filter(date__date=date.today()).first()
        if not quote_of_day:
            response = self.get_response()[0]
            quote_of_day = QuoteOfDay(quote=response.get('content'), author=response.get('author'))
            quote_of_day.save()
        context = {
            'title': 'Quote of the Day',
            'quote': quote_of_day,
            'favorites': request.user.favorites.all() if request.user.is_authenticated else None,
        }
        return render(request, self.template_name, context)


class QuotesListView(BaseQuoteView):
    """A view class for displaying a list of quotes."""

    template_name = 'qtable_app/quotes_list.html'
    url = 'https://api.quotable.io/quotes'

    def get(self, request: HttpRequest, page: int = None) -> HttpResponse:
        """
        Render a template displaying a list of quotes from an external API.

        :param request: The HTTP request object.
        :type request: HttpRequest
        :param page: The page number to retrieve. Defaults to None.
        :type page: int, optional
        :return: The HTTP response object containing the rendered template.
        :rtype: HttpResponse
        """
        context = {
            'title': 'Quotes List',
            'quotes': self.get_response(page),
            'favorites': request.user.favorites.all() if request.user.is_authenticated else None,
        }
        return render(request, self.template_name, context)


class FavoritesListView(LoginRequiredMixin, ListView):
    """View for displaying a list of favorite users for the current user."""

    template_name = 'qtable_app/favorites.html'
    url = 'https://api.quotable.io/quotes'
    paginate_by = 4

    def get_queryset(self) -> QuerySet:
        """
        Return the queryset of favorite users for the current user.

        :param self: The current instance of the class.
        :return: A queryset of User objects representing the favorite users of the current user.
        :rtype: QuerySet[User]
        """
        return self.request.user.favorites.all()

    def get_context_data(self, **kwargs) -> dict:
        """
        Retrieve and returns the context data for the view.

        :param kwargs: Additional keyword arguments.
        :type kwargs: dict

        :return: A dictionary containing the context data for the view.
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Favorites'
        context['favorites'] = self.request.user.favorites.all()
        return context


class FavoriteSetView(LoginRequiredMixin, View):
    """View for toggling favorite status for a specific quote of the day."""

    def get(self, request: HttpRequest, pk: int) -> HttpResponseRedirect:
        """
        Retrieve a specific quote of the day and toggles its favorite status for the authenticated user.

        :param request: The HTTP request object.
        :type request: HttpRequest
        :param pk: The primary key of the quote of the day to retrieve.
        :type pk: int
        :return: A redirect response to the next URL specified in the request's GET parameters.
        :rtype: HttpResponseRedirect
        """
        user = get_object_or_404(User, pk=request.user.pk)
        favorite = get_object_or_404(QuoteOfDay, pk=pk)
        if favorite in user.favorites.all():
            user.favorites.remove(favorite)
        else:
            user.favorites.add(favorite)
        user.save()
        next_url = request.GET.get('next', reverse('qtable_app:index'))
        return redirect(next_url)
