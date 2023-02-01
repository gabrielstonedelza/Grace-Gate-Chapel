from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CheckInToday, Announcements, Events, Notifications, MorningDevotion
from django.conf import settings
from django.utils import timezone
from users.models import GGCUser, Profile

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=CheckInToday)
def alert_check_in_today(sender, created, instance, **kwargs):
    admin = GGCUser.objects.get(id=1)
    if created:
        title = "Check In Today"
        message = f"{instance.user.username} just checked in today"
        Notifications.objects.create(notification_id=instance.id, notification_title=title,
                                     notification_message=message,
                                     notification_from=instance.user,
                                     notification_to=admin,
                                     )
