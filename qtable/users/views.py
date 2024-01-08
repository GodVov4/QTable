from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterForm


class RegisterView(CreateView):
    template_name = 'users/signup.html'
    form_class = RegisterForm
    extra_context = {'title': 'Sign up'}
    success_url = reverse_lazy('users:login')
