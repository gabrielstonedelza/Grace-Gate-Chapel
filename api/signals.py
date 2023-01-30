from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CheckInToday, Announcements, Events, Notifications, AddMember

# @receiver(post_save, sender=CheckInToday)
# def alert_check_in_today(sender, created, instance, **kwargs):
#     admin = AddMember.objects.get(id=1)
#     if created:
#         title = "Check In Today"
#         message = f"{instance.member.name} just checked in today"
#
#         Notifications.objects.create(notification_id=instance.id, notification_title=title,
#                                      notification_message=message,
#                                      notification_from=instance.member.name,
#                                      notification_to=admin,
#                                      )
