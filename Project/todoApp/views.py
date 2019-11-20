from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import User, Item
from datetime import *
from django.utils.dateparse import parse_datetime
import operator


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
    todo_list = Item.objects.filter(user_id=user_id).values_list(
        "id", "content", "date_created", "complete", "completed_date", "deadline"
    )
    item_list = []
    # print(todo_list)
    for objects in todo_list:
        item = Item(
            id=objects[0],
            content=objects[1],
            date_created=objects[2],
            complete=objects[3],
            completed_date=objects[4],
            deadline=objects[5],
        )
        item_list.append(item)
        # print(item_list)
    # sortDate(item_list, ol)
    return render(
        request,
        "todo.html",
        {"user_id": user_id, "user_name": user_data[0][0], "todo_items": item_list,},
    )


def sortDate(item_list, ol):
    ###Create recursive sorter??
    i = 0
    for item in item_list:
        ol.append(item.deadline)
    while i < len(item_list):
        print(item_list[i].deadline)
        i += 1


def addTodo(request, user_id):
    if not request.POST["content"]:
        return HttpResponse("Please make sure you fill out the textfield!")
    else:
        try:
            t = time.fromisoformat(request.POST["deadline_time"])
        except:
            t = time.fromisoformat("12:00")
        try:
            d = date.fromisoformat(request.POST["deadline_date"])
            dt = datetime.combine(d, t)
            new_item = Item(
                user=User.objects.get(id=user_id),
                content=request.POST["content"],
                date_created=datetime.now(),
                deadline=dt,
            )
            new_item.save()
        except:
            new_item = Item(
                user=User.objects.get(id=user_id),
                content=request.POST["content"],
                date_created=datetime.now(),
            )
            new_item.save()
    url = "/todo/" + str(user_id) + "/"
    return HttpResponseRedirect(url)


def completeTodo(request, user_id, item_id):
    del_item = Item.objects.get(id=item_id)
    del_item.completed_date = datetime.now()
    del_item.complete = True
    del_item.save()
    url = "/todo/" + str(user_id) + "/"
    return HttpResponseRedirect(url)


def deleteTodo(request, user_id, item_id):
    del_item = Item.objects.get(id=item_id)
    del_item.delete()
    url = "/todo/" + str(user_id) + "/"
    return HttpResponseRedirect(url)
