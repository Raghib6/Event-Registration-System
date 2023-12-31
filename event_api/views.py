from django.shortcuts import render
from rest_framework import generics, status
from event_app.models import Event, EventRegistration
from .serializers import EventSerializer, EventRegistrationSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class EventList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDetails(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = "id"


class JoinEvent(generics.CreateAPIView):
    serializer_class = EventRegistrationSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        event = serializer.validated_data["event"]

        if EventRegistration.objects.filter(user=user, event=event).exists():
            return Response(
                {"detail": "You have already joined the event"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if event.available_slots > 0:
            event.available_slots -= 1
            event.save()
            instance = serializer.save(user=user)
            response_data = serializer.data
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"detail": "No slots available"}, status=status.HTTP_400_BAD_REQUEST
            )


class UserEventList(generics.ListAPIView):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        events = user.events.all()
        return events
