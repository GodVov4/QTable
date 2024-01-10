"""
This module defines the QuoteOfDay model and its associated fields for storing daily quotes within the application.

Model:
    - QuoteOfDay: Represents a daily quote with fields for quote content, author, creation date, last updated date,
        and user favorites.

Fields and Relationships:
    - quote: Represents the content of the daily quote.
    - author: Represents the author of the daily quote.
    - date: Represents the creation date of the daily quote.
    - updated: Represents the last updated date of the daily quote.
    - users: Establishes a many-to-many relationship with the built-in User model, allowing users to mark quotes as
        favorites.

Usage:
    The module provides the QuoteOfDay model for storing daily quotes and facilitating user interactions such as marking
    quotes as favorites.
    Developers can utilize this model to manage daily quotes and associated user favorites within the application.

Note:
    The module focuses on defining the QuoteOfDay model and its associated fields, enabling the application to manage
    daily quotes and user preferences effectively.
"""
from django.contrib.auth.models import User
from django.db.models import CharField, DateTimeField, ManyToManyField, Model, TextField


class QuoteOfDay(Model):
    """Represents a daily quote with fields for quote content, author, creation date, last updated date."""

    quote = TextField()
    author = CharField(max_length=100)
    date = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    users = ManyToManyField(User, 'favorites')
