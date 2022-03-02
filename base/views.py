from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm


def logout_user(request):
    if not request.user.is_authenticated:
        return redirect("base-home")
    logout(request)
    return redirect("base-home")


def register_page(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("base-home")
        else:
            messages.error(request, "An error occured during registration!")
    return render(request, "base/login_register.html", {"form": form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect("base-home")

    page = "login"
    context = {"page": page}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

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
    if (q := request.GET.get("q")) is None:
        q = ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(description__icontains=q) | Q(name__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
        "room_messages": room_messages,
    }
    return render(request, "base/home.html", context)


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {"user": user, "rooms": rooms, "room_messages": room_messages, 'topics': topics}
    return render(request, "base/profile.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by("-created")
    participants = room.participants.all()

    if request.method == "POST":
        Message.objects.create(
            room=room, user=request.user, body=request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("base-room", pk=room.id)

    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "base/room.html", context)


@login_required(login_url="base-login")
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed to delete this message")

    if request.method == "POST":
        message.delete()
        return redirect("base-home")
    return render(request, "base/delete.html", {"obj": message})


@login_required(login_url="base-login")
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("base-home")
    context = {"form": form}
    return render(request, "base/room_form.html", context)


@login_required(login_url="base-login")
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed to edit this room")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("base-home")

    context = {"form": form}
    return render(request, "base/room_form.html", context)


def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed to edit this room")

    if request.method == "POST":
        room.delete()
        return redirect("base-home")
    return render(request, "base/delete.html", {"obj": room})
