from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django_email_verification import send_email

from .forms import RegisterForm


class RegisterView(CreateView):
    template_name = 'users/signup.html'
    form_class = RegisterForm
    extra_context = {'title': 'Sign up'}

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        self.success_url = reverse_lazy('users:confirm_email', kwargs={"pk": user.id})
        return_val = super(RegisterView, self).form_valid(form)
        send_email(user)
        return return_val


def confirm_email(request, pk):
    context = {
        'title': 'Confirm email',
        'user': User.objects.get(pk=pk),
    }
    return render(request, 'users/confirm_email.html', context)
