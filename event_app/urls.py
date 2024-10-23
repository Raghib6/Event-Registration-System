from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("event/<int:id>/", views.event_details, name="event_details"),
    path("join-event/<int:id>/", views.join_event, name="join_event"),
    path("leave-event/<int:id>/", views.leave_event, name="leave_event"),
    path("user-profile/", views.user_profile, name="user_profile"),
    path("create-event/", views.create_event, name="create_event"),
    path("update-event/<int:id>/", views.update_event, name="update_event"),
    path("delete-event/<int:id>/", views.delete_event, name="delete_event"),
    path("event-details/<int:id>/", views.see_participant_list, name="event_more_details"),
]
