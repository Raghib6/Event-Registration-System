from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import UserSignUpForm
from django.contrib.auth import authenticate
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,staff_check
from .models import Event, EventRegistration
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from .forms import EventForm

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
    checked = False
    user = request.user
    if user.is_superuser or user.is_staff:
        checked = True
    current_date = datetime.now().date()
    last_date = event.date - timedelta(days=1)
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
        "checked":checked
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
            event.available_slots -=1
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
    events = None
    admin_events = None
    query = request.GET.get("search")
    if user.is_superuser or user.is_staff:
        admin_events = Event.objects.filter(user=user).order_by("-created_at")
        count = admin_events.count()
        if query:
            admin_events = Event.objects.filter(
            Q(user=user) & (Q(title__icontains=query) | Q(location__icontains=query))
        )
    else:
        events = user.events.all().order_by("-created_at")
        count = events.count()
        if query:     
            events = EventRegistration.objects.filter(
                Q(user=user) & (Q(event__title__icontains=query) | Q(event__location__icontains=query))
            )

    context = {"username": user.username, "events": events,"admin_events":admin_events,"count":count}
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
            return redirect("/")
        else:
            messages.error(request, "Invalid Login credential")
            return redirect("login")
    return render(request, "login.html")


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out")
    return redirect("login")

@staff_check
def create_event(request):
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST,request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(
                request, "Congratulations! Your event creation is successfull"
            )
            return redirect("user_profile")
    return render(request, "event-form.html", {"form": form})

@staff_check
def update_event(request,id):
    event = get_object_or_404(Event,id=id)
    counter = EventRegistration.objects.filter(event=event).count()
    flag = True
    if event.user == request.user:
        form = EventForm(instance=event)
        if request.method == "POST":
            form = EventForm(request.POST,request.FILES,instance=event)
            if form.is_valid():
                event.available_slots = event.total_slots - counter
                event.save()
                form.save()
                return redirect("event_details",id)
        context = {"form":form,"flag":flag}

        return render(request,'event-form.html',context)
    else:
        return redirect("home")

@staff_check
def delete_event(request,id):
    event = get_object_or_404(Event,id=id)
    if not event.user == request.user:
        return redirect("home")
    elif request.method=="POST" and event.user == request.user:
        event.delete()
        return redirect("user_profile")
    context = {"event":event}
    return render(request,'delete-event.html',context)

@staff_check
def see_participant_list(request,id):
    event = get_object_or_404(Event,id=id)
    if event.user == request.user:
        event_details = EventRegistration.objects.filter(event=id)
        count = event_details.count()
        context = {"event":event,"event_details":event_details,"count":count}
        return render(request,'participant-list.html',context)
    else:
        return redirect("/")