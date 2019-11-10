from django.db import models


class Item(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    date_created = models.TimeField(auto_now_add=False)


class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    todo_list = models.ForeignKey(Item, on_delete=models.CASCADE)

