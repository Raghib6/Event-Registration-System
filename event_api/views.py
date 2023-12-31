from django.shortcuts import render
from rest_framework import generics
from event_app.models import Event
from .serializers import EventSerializer


class EventList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
