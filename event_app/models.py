from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    time = models.TimeField(auto_now_add=False)
    date = models.DateField(auto_now_add=False)
    location = models.CharField(max_length=250)
    total_slots = models.PositiveIntegerField()
    available_slots = models.PositiveIntegerField()
    image = models.ImageField(upload_to="events")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.available_slots = self.total_slots
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class EventRegistration(models.Model):
    user = models.ForeignKey(User, related_name="events", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event.title
