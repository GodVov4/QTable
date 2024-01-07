# Generated by Django 5.0.1 on 2024-01-07 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuoteOfDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.TextField()),
                ('author', models.CharField(max_length=120)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]