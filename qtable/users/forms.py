from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    first_name = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'class': "form-control"}))
    last_name = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'class': "form-control"}))
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': "form-control"}))
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': "form-control"}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email', )
        if email and get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email
