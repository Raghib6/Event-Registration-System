from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.index, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("event/<int:id>/", views.event_details, name="event_details"),
]
