from rest_framework import serializers
from event_app.models import Event, EventRegistration


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "time",
            "date",
            "location",
            "total_slots",
            "available_slots",
            "image",
            "created_at",
        ]
