from django.db import models

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
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=16, unique=True)
    home_address = models.CharField(max_length=100, blank=True)
    digital_address = models.CharField(max_length=100, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CheckInToday(models.Model):
    member = models.ForeignKey(AddMember, on_delete=models.CASCADE)
    has_checked_in = models.BooleanField(default=False)
    time_checked_in = models.TimeField(auto_now_add=True)
    date_checked_in = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.member.name


class Announcements(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
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
    notification_from = models.ForeignKey(AddMember, on_delete=models.CASCADE, null=True)
    notification_to = models.ForeignKey(AddMember, on_delete=models.CASCADE, related_name="DeUser_receiving_notification",)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notification_title