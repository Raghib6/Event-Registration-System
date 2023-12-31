from django.urls import path
from .views import EventList, EventDetails, JoinEvent, UserEventList

urlpatterns = [
    path("events/", EventList.as_view(), name="events"),
    path("events/<int:id>/", EventDetails.as_view(), name="event_detail"),
    path("join-events/", JoinEvent.as_view(), name="join_events"),
    path("user-events/", UserEventList.as_view(), name="user-events"),
]
