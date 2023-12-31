from rest_framework import serializers
from django.contrib.auth.models import User
from event_app.models import Event, EventRegistration


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


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


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ["id", "event", "user", "created_at"]
        read_only_fields = ["id", "user", "created_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["event"] = instance.event.title
        data["user"] = instance.user.username
        return data
