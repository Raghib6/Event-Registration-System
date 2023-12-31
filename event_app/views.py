from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import UserSignUpForm
from django.contrib.auth import authenticate
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from .models import Event, EventRegistration
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404


def index(request):
    query = request.GET.get("search")
    events = Event.objects.all()
    if query:
        events = Event.objects.filter(
            Q(title__icontains=query) | Q(location__icontains=query)
        )
    return render(request, "index.html", {"events": events})


def event_details(request, id):
    event = Event.objects.get(id=id)
    user = request.user
    current_date = datetime.now().date()
    last_date = event.date - timedelta(days=1)
    if current_date > last_date:
        print("current date greater")
    elif current_date < last_date:
        print("current date smaller")
    elif current_date == last_date:
        print("equal")
    if user.is_authenticated:
        try:
            joined = EventRegistration.objects.filter(
                user=user, event=event.id
            ).exists()
        except EventRegistration.DoesNotExist:
            joined = None
    else:
        joined = None
    context = {
        "event": event,
        "joined": joined,
        "current_date": current_date,
        "last_date": last_date,
    }
    return render(request, "event_details.html", context)


@login_required(login_url="login")
def join_event(request, id):
    user = request.user
    event = get_object_or_404(Event, id=id)
    try:
        if (
            event.available_slots > 0
            and not EventRegistration.objects.filter(user=user, event=event).exists()
        ):
            er = EventRegistration.objects.create(user=user, event=event)
            event.available_slots -= 1
            event.save()
            return render(request, "success.html", {"user": user, "event": event})
        else:
            return redirect(f"/event/{event.id}")
    except Event.DoesNotExist:
        pass


@login_required(login_url="login")
def leave_event(request, id):
    user = request.user
    event = get_object_or_404(Event, id=id)
    try:
        if EventRegistration.objects.filter(user=user, event=event).exists():
            er = get_object_or_404(EventRegistration, user=user, event=event)
            er.delete()
            event.available_slots += 1
            event.save()
            return redirect("/user-profile/")
        else:
            return redirect(f"/event/{event.id}")
    except Event.DoesNotExist:
        pass


@login_required(login_url="login")
def user_profile(request):
    user = request.user
    events = user.events.all().order_by("-created_at")
    query = request.GET.get("search")
    if query:
        events = EventRegistration.objects.filter(
            Q(event__title__icontains=query) | Q(event__location__icontains=query)
        )
    context = {"username": user.username, "events": events}
    return render(request, "profile.html", context)


@unauthenticated_user
def signup(request):
    form = UserSignUpForm()
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Congratulations! Your account creation successfull"
            )
            return redirect("login")
    return render(request, "signup.html", {"form": form})


@unauthenticated_user
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password1"]
        user = authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            # messages.success(request, "You are now logged in")
            return redirect("/home/")
        else:
            messages.error(request, "Invalid Login credential")
            return redirect("login")
    return render(request, "login.html")


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out")
    return redirect("login")
