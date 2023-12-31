from django.urls import path
from .views import EventList, EventDetails

urlpatterns = [
    path("events/", EventList.as_view(), name="events"),
    path("events/<int:id>/", EventDetails.as_view(), name="event_details"),
]
