"""
This module defines a custom registration form for user registration within the application.

RegisterForm Class:
    - Inherits from UserCreationForm to provide user registration functionality with added fields.
    - Includes fields such as username, email, first name, last name, and password for user registration.
    - Implements custom validation to ensure unique email addresses during registration.

Attributes:
    - username: A CharField representing the username with a maximum length of 24 characters.
    - email: A CharField representing the email address with a maximum length of 100 characters.
    - first_name: A CharField representing the user's first name with a maximum length of 24 characters.
    - last_name: A CharField representing the user's last name with a maximum length of 24 characters.
    - password1: A CharField representing the password with a maximum length of 24 characters (first entry).
    - password2: A CharField representing the password with a maximum length of 24 characters (confirmation entry).

Methods:
    - clean_email(): Validates the email field to ensure it does not already exist in the database.
                     Raises a forms.ValidationError if the email already exists.

Meta Class:
    - Specifies the model and fields for the form, including 'username', 'email', 'first_name', 'last_name',
        'password1',and 'password2'.

Usage:
    The RegisterForm class is designed for user registration, ensuring that users provide unique email addresses and
    necessary details.
    The form inherits from Django's UserCreationForm and adds additional fields and validation to facilitate user
    registration.

Note:
    The form utilizes Django's built-in UserCreationForm and extends it to include additional fields and custom
    validation for email uniqueness.
"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    """
    A form used for user registration.

    Inherits from UserCreationForm and adds additional fields for username,
    email, first name, last name, and password.
    """

    username = forms.CharField(
        max_length=24,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    email = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    first_name = forms.CharField(
        max_length=24,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    last_name = forms.CharField(
        max_length=24,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password1 = forms.CharField(
        max_length=24,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        max_length=24,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self) -> str:
        """
        Clean the email field and check if it already exists in the database.

        :return: The cleaned email value.
        :rtype: str

        :raises forms.ValidationError: If the email already exists in the database.
        """
        email = self.cleaned_data.get('email')
        if email and get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email
