from django.contrib.auth.models import User
from django.db import models
from django.db.models import ManyToManyField


class QuoteOfDay(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=120)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    users = ManyToManyField(User, 'favorites')
