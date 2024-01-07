from django.db import models


class QuoteOfDay(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=120)
    date = models.DateTimeField(auto_now_add=True)
