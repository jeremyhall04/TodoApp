from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import User, Item
from datetime import *


def Landing(request):
    return render(request, "landing.html")


def Login(request):
    if User.objects.filter(username=request.POST["username"]).exists() == False:
        return HttpResponse("Incorrect Username")
    else:
        user = User.objects.filter(username=request.POST["username"]).values_list(
            "id", "username", "password"
        )
        pw = user.values_list("password")[0]
        if request.POST["password"] != pw[0]:
            # pw is the first tuple in QuerySet
            # pw[0] is the first item in the tuple
            return HttpResponse("Incorrect PW")
        else:
            return HttpResponseRedirect("/todo/", content=user)


def Register(request):
    return render(request, "register.html")


def Create(request):
    if User.objects.filter(username=request.POST["username"]).exists():
        return HttpResponse("User already exists")
    elif User.objects.filter(email=request.POST["email"]).exists():
        return HttpResponse("Email is already in use")
    else:
        new_user = User(
            username=request.POST["username"],
            password=request.POST["password"],
            email=request.POST["email"],
        )
        new_user.save()
        return HttpResponseRedirect("/landing/")


def TodoView(request):
    if User.objects.filter(username=request.POST["username"]).exists() == False:
        return HttpResponse("Incorrect Username")
    else:
        user_q = User.objects.filter(username=request.POST["username"]).values_list(
            "id", "username", "password"
        )
        for user in user_q:
            print(user)
        if request.POST["password"] != user[2]:
            # pw is the first tuple in QuerySet
            # pw[0] is the first item in the tuple
            return HttpResponse("Incorrect PW")
        else:
            todo_list = Item.objects.filter(user_id=user[0]).values_list()
            return render(
                request,
                "todo.html",
                {"user_id": user[0], "user_name": user[1], "todo_items": todo_list},
            )


def addTodo(request, user_id):
    new_item = Item(
        user=User.objects.get(id=user_id),
        content=request.POST["content"],
        date_created=datetime.now(),
    )
    new_item.save()
    return HttpResponseRedirect("/todo/")
