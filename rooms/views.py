import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Room
from django.contrib.auth import logout


def generate_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def home(request):
    return render(request, "rooms/home.html")


def create_room(request):
    if request.method == "POST":
        name = request.POST.get("name")
        code = generate_code()

        while Room.objects.filter(code=code).exists():
            code = generate_code()

        host = request.user if request.user.is_authenticated else User.objects.first()

        Room.objects.create(name=name, code=code, host=host)
        return redirect("room_detail", code=code)

    return render(request, "rooms/create_room.html")


def join_room(request):
    error = None

    if request.method == "POST":
        code = request.POST.get("code", "").upper()
        try:
            room = Room.objects.get(code=code)
            return redirect("room_detail", code=room.code)
        except Room.DoesNotExist:
            error = "Room not found"

    return render(request, "rooms/join_room.html", {"error": error})


@login_required
def room_detail(request, code):
    room = get_object_or_404(Room, code=code)
    is_host = (room.host == request.user)
    return render(request, "rooms/room_detail.html", {
        "room": room,
        "is_host": is_host
    })



def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "rooms/register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("/")


def custom_login(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_url = request.GET.get("next", "/")
            return redirect(next_url)

    return render(request, "registration/login.html", {"form": form})
