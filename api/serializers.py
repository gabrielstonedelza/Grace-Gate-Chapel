from rest_framework import serializers
from .models import AddMember, CheckInToday, Announcements, Events, Notifications, MorningDevotion

class AddMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddMember
        fields = ['id', 'name', 'email', 'phone_number', 'home_address', 'digital_address', 'date_added']


class CheckInTodaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckInToday
        fields = ['id', 'user', 'has_checked_in', 'time_checked_in', 'date_checked_in','get_uesrname']
        read_only_fields = ['user']


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcements
        fields = ['id', 'title' ,'message', 'date_added','views']


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id', 'event_title', 'event_time', 'event_date', 'date_added']


class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['id', 'notification_id', 'notification_title', 'notification_message', 'read', 'notification_trigger', 'notification_from', 'notification_to', 'date_created']


class MorningDevotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MorningDevotion
        fields = ['id', 'title', 'quotations', 'message', 'date_created','views']