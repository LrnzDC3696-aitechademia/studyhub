from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Room, Topic
from .forms import RoomForm


def logout_page(request):
    logout(request)
    return render(request, "base/login_register.html")


def login_page(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:  # type: ignore
            messages.error(request, "user does not exist")
            return render(request, "base/login_register.html", context)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("base-home")
        else:
            messages.error(request, "invalid credentials")

    return render(request, "base/login_register.html", context)


def home(request):
    if (q := request.GET.get('q')) is None:
        q = ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(description__icontains=q) |
        Q(name__icontains=q)
    )
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {"rooms": rooms, "topics": topics, "room_count": room_count}
    return render(request, "base/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, "base/room.html", context)


def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("base-home")
    context = {"form": form}
    return render(request, "base/room_form.html", context)


def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("base-home")

    context = {"form": form}
    return render(request, "base/room_form.html", context)


def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect("base-home")
    return render(request, "base/delete_room.html", {"obj": room})
