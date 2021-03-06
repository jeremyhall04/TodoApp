from django.db import models
from datetime import *
from django.utils.timezone import *


class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)


class Item(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=False)
    complete = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True)
    deadline = models.DateTimeField(null=True)
