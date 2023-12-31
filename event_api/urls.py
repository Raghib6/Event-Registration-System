from django.urls import path
from .views import EventList

urlpatterns = [path("", EventList.as_view(), name="events")]
