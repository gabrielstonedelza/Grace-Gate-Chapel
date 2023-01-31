from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response

from .models import AddMember, CheckInToday, Announcements, Events, Notifications
from .serializers import AddMemberSerializer, CheckInTodaySerializer, AnnouncementSerializer, EventsSerializer, NotificationsSerializer
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import Http404



@api_view(['POST'])
def add_member(request):
    serializer = AddMemberSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllMembersView(generics.ListCreateAPIView):
    queryset = AddMember.objects.all().order_by('-date_added')
    serializer_class = AddMemberSerializer

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = AddMemberSerializer(queryset, many=True)
        return Response(serializer.data)
#
#
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def member_detail(request, pk):
    member = AddMember.objects.get(pk=pk)
    serializer = AddMemberSerializer(member, many=False)
    return Response(serializer.data)



@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def update_member(request, pk):
    member = get_object_or_404(AddMember, pk=pk)
    serializer = AddMemberSerializer(member, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def member_delete(request, pk):
    try:
        member = AddMember.objects.get(pk=pk)
        member.delete()
    except AddMember.DoesNotExist:
        pass
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def add_member_check_in(request,phone_number):
    member = get_object_or_404(AddMember, phone_number=phone_number)
    serializer = CheckInTodaySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(member=member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllCheckInSTodayView(generics.ListCreateAPIView):
    my_date = datetime.today()
    de_date = my_date.date()
    queryset = check_ins_today = CheckInToday.objects.filter(date_checked_in=de_date).order_by('-date_checked_in')
    serializer_class = CheckInTodaySerializer

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = CheckInTodaySerializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def add_event(request):
    serializer = EventsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllEventsView(generics.ListCreateAPIView):
    queryset = Events.objects.all().order_by('-date_added')
    serializer_class = EventsSerializer

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = EventsSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def add_announcement(request):
    serializer = AnnouncementSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllAnnouncementsView(generics.ListCreateAPIView):
    queryset = Announcements.objects.all().order_by('-date_added')
    serializer_class = AnnouncementSerializer

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = AnnouncementSerializer(queryset, many=True)
        return Response(serializer.data)


# notifications
@api_view(['GET'])

def get_all_user_notifications(request):
    notifications = Notifications.objects.filter(notification_to_passenger=request.user).order_by(
        '-date_created')[:50]
    serializer = NotificationsSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])

def get_all_driver_notifications(request):
    notifications = Notifications.objects.filter(notification_to=request.user).order_by(
        '-date_created')
    serializer = NotificationsSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_user_notifications(request):
    notifications = Notifications.objects.filter(notification_to=request.user).filter(
        read="Not Read").order_by(
        '-date_created')[:50]
    serializer = NotificationsSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_triggered_notifications(request):
    notifications = Notifications.objects.filter(notification_to=request.user).filter(
        notification_trigger="Triggered").filter(
        read="Not Read").order_by('-date_created')[:50]
    serializer = NotificationsSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def read_notification(request):
    notifications = Notifications.objects.filter(notification_to=request.user).filter(
        read="Not Read").order_by('-date_created')[:50]
    for i in notifications:
        i.read = "Read"
        i.save()

    serializer = NotificationsSerializer(notifications, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
def approve_check_in(request, pk):
    member_checking_in = get_object_or_404(AddMember, pk=pk)
    check_in_member = get_object_or_404(CheckInToday,  member=member_checking_in.id)
    serializer = CheckInTodaySerializer(check_in_member, data=request.data)
    if serializer.is_valid():
        serializer.save(member=member_checking_in)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_my_check_ins(request, phone_number):
    member = get_object_or_404(AddMember, phone_number=phone_number)
    my_check_ins = CheckInToday.objects.filter(member=member)
    serializer = CheckInTodaySerializer(my_check_ins, many=True)
    return Response(serializer.data)