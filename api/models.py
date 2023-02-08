from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

READ_STATUS = (
    ("Read", "Read"),
    ("Not Read", "Not Read"),
)

NOTIFICATIONS_STATUS = (
    ("Read", "Read"),
    ("Not Read", "Not Read"),
)

NOTIFICATIONS_TRIGGERS = (
    ("Triggered", "Triggered"),
    ("Not Triggered", "Not Triggered"),
)

class AddMember(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, blank=True)
    phone_number = models.CharField(max_length=16, unique=True, blank=True)
    home_address = models.CharField(max_length=100, blank=True)
    digital_address = models.CharField(max_length=100, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CheckInToday(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    has_checked_in = models.BooleanField(default=False)
    time_checked_in = models.TimeField(auto_now_add=True)
    date_checked_in = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_uesrname(self):
        return self.user.username


class Announcements(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    views = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Events(models.Model):
    event_title = models.CharField(max_length=255)
    event_time = models.CharField(max_length=20, blank=True)
    event_date = models.CharField(max_length=20, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_title


class Notifications(models.Model):
    notification_id = models.CharField(max_length=100, blank=True, default="")
    notification_title = models.CharField(max_length=255, blank=True)
    notification_message = models.TextField(blank=True)
    read = models.CharField(max_length=20, choices=NOTIFICATIONS_STATUS, default="Not Read")
    notification_trigger = models.CharField(max_length=255, choices=NOTIFICATIONS_TRIGGERS, default="Triggered",
                                            blank=True)
    notification_from = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    notification_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="DeUser_receiving_notification", null=True)
    notification_to_admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Admin_receiving_notification",default=1)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notification_title

class MorningDevotion(models.Model):
    title = models.CharField(max_length=255)
    quotations = models.TextField()
    message = models.TextField()
    views = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title