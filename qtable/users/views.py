"""
This module contains views and functions related to user registration and email confirmation.

The module includes the following:

- `RegisterView`: A view for the registration of new users.
- `confirm_email`: A function to render the confirmation email page for a specific user.

Dependencies:
- `django.contrib.auth.models.User`: The User model provided by Django for user authentication.
- `django.http.HttpResponse`: The class representing an HTTP response.
- `django.http.HttpRequest`: The class representing an HTTP request.
- `django.shortcuts.get_object_or_404`: A shortcut function to get an object or return 404.
- `django.shortcuts.render`: A shortcut function to render a template.
- `django.urls.reverse_lazy`: A lazily evaluated version of `django.urls.reverse`.
- `django.views.generic.CreateView`: A generic class-based view for creating a model.
"""
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django_email_verification import send_email

from .forms import RegisterForm


class RegisterView(CreateView):
    """A view for the registration of new users."""

    template_name = 'users/signup.html'
    form_class = RegisterForm
    extra_context = {'title': 'Sign up'}

    def form_valid(self, form) -> HttpResponseRedirect:
        """
        Save the form data and performs additional actions.

        :param form: The form object containing the data to be saved.
        :type form:

        :return: The response returned by the super class after saving the form.
        :rtype: HttpResponseRedirect
        """
        user = form.save()
        user.is_active = False
        self.success_url = reverse_lazy('users:confirm_email', kwargs={'pk': user.id})
        return_val = super().form_valid(form)
        send_email(user)
        return return_val


def confirm_email(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Render the confirmation email page for a specific user.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param pk: The primary key of the user to confirm the email for.
    :type pk: int
    :return: An HTTP response containing the rendered confirmation email page.
    :rtype: HttpResponse
    """
    context = {
        'title': 'Confirm email',
        'user': get_object_or_404(User, pk=pk),
    }
    return render(request, 'users/confirm_email.html', context)
