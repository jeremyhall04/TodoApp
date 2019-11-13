from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import User, Item
from datetime import *


def Landing(request):
    return render(request, "landing.html")


def Login(request):
    if User.objects.filter(username=request.POST["username"]).exists() == False:
        return HttpResponse("Incorrect Username")
    else:
        user_q = User.objects.filter(username=request.POST["username"]).values_list(
            "id", "username", "password"
        )
        for user in user_q:
            print("apples")
        if request.POST["password"] != user[2]:
            # pw is the first tuple in QuerySet
            # pw[0] is the first item in the tuple
            return HttpResponse("Incorrect PW")
        else:
            url = "/todo/" + str(user[0]) + "/"
            return HttpResponseRedirect(url)


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
        return HttpResponseRedirect("/")


def TodoView(request, user_id):
    user_data = User.objects.filter(id=user_id).values_list("username")
    todo_list = Item.objects.filter(user_id=user_id).values_list("id", "content")
    item_list = []
    for objects in todo_list:
        item = Item(id=objects[0], content=objects[1])
        item_list.append(item)
    return render(
        request,
        "todo.html",
        {"user_id": user_id, "user_name": user_data[0][0], "todo_items": item_list},
    )


def addTodo(request, user_id):
    new_item = Item(
        user=User.objects.get(id=user_id),
        content=request.POST["content"],
        date_created=datetime.now(),
    )
    new_item.save()
    url = "/todo/" + str(user_id) + "/"
    return HttpResponseRedirect(url)


def deleteTodo(request, user_id, item_id):
    del_item = Item.objects.get(id=item_id)
    del_item.delete()
    url = "/todo/" + str(user_id) + "/"
    return HttpResponseRedirect(url)
