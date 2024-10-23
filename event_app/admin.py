from django.contrib import admin
from .models import Event, EventRegistration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "user",
        "time",
        "date",
        "available_slots",
        "total_slots",
        "created_at",
    ]
    search_fields = ["title"]


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "event",
        "created_at",
    ]
