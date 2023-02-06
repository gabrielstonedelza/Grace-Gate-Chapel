from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import AddMember, CheckInToday, Announcements, Events, Notifications, MorningDevotion
from .serializers import  CheckInTodaySerializer, AnnouncementSerializer, EventsSerializer, NotificationsSerializer, MorningDevotionSerializer
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import Http404
from users.models import GGCUser, Profile

#
#
# @api_view(['POST'])
# def add_member(request):
#     serializer = AddMemberSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AllMembersView(generics.ListCreateAPIView):
#     queryset = AddMember.objects.all().order_by('-date_added')
#     serializer_class = AddMemberSerializer
#
#     @method_decorator(cache_page(60 * 60 * 2))
#     def list(self, request):
#         # Note the use of `get_queryset()` instead of `self.queryset`
#         queryset = self.get_queryset()
#         serializer = AddMemberSerializer(queryset, many=True)
#         return Response(serializer.data)
# #
#
# @api_view(['GET'])
# @permission_classes([permissions.AllowAny])
# def member_detail(request, pk):
#     member = AddMember.objects.get(pk=pk)
#     serializer = AddMemberSerializer(member, many=False)
#     return Response(serializer.data)
#


# @api_view(['GET', 'PUT'])
# @permission_classes([permissions.AllowAny])
# def update_member(request, pk):
#     member = get_object_or_404(AddMember, pk=pk)
#     serializer = AddMemberSerializer(member, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'DELETE'])
# def member_delete(request, pk):
#     try:
#         member = AddMember.objects.get(pk=pk)
#         member.delete()
#     except AddMember.DoesNotExist:
#         pass
#     return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def add_member_check_in(request):
    serializer = CheckInTodaySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllCheckInSTodayView(generics.ListCreateAPIView):
    my_date = datetime.today()
    de_date = my_date.date()
    queryset = check_ins_today = CheckInToday.objects.filter(date_checked_in=de_date).order_by('-date_checked_in')
    serializer_class = CheckInTodaySerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = CheckInTodaySerializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_event(request):
    serializer = EventsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllEventsView(generics.ListCreateAPIView):
    queryset = Events.objects.all().order_by('-date_added')
    serializer_class = EventsSerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = EventsSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_announcement(request):
    serializer = AnnouncementSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllAnnouncementsView(generics.ListCreateAPIView):
    queryset = Announcements.objects.all().order_by('-date_added')
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = AnnouncementSerializer(queryset, many=True)
        return Response(serializer.data)


# notifications
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_all_user_notifications(request):
    notifications = Notifications.objects.filter(notification_to=request.user).order_by(
        '-date_created')[:50]
    serializer = NotificationsSerializer(notifications, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_unread_notifications(request):
    notifications = Notifications.objects.filter(notification_to=request.user).filter(
        read="Not Read").order_by(
        '-date_created')[:50]
    serializer = NotificationsSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_triggered_notifications(request):
    notifications = Notifications.objects.filter(notification_to=request.user).filter(
        notification_trigger="Triggered").filter(
        read="Not Read").order_by('-date_created')[:50]
    serializer = NotificationsSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def read_notification(request):
    notifications = Notifications.objects.filter(notification_to=request.user).filter(
        read="Not Read").order_by('-date_created')[:50]
    for i in notifications:
        i.read = "Read"
        i.save()

    serializer = NotificationsSerializer(notifications, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def approve_check_in(request, pk):
    check_in_member = get_object_or_404(CheckInToday,  user=pk)
    serializer = CheckInTodaySerializer(check_in_member, data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_my_check_ins(request):
    my_check_ins = CheckInToday.objects.filter(user=request.user)
    serializer = CheckInTodaySerializer(my_check_ins, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_devotion(request):
    serializer = MorningDevotionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllDevotionView(generics.ListCreateAPIView):
    queryset = MorningDevotion.objects.all().order_by('-date_created')
    serializer_class = MorningDevotionSerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = MorningDevotionSerializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def devotion_detail(request,pk):
    devotion = get_object_or_404(MorningDevotion, pk=pk)
    if devotion:
        devotion.views += 1
        devotion.save()
    serializer = MorningDevotionSerializer(devotion,many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def announcement_detail(request,pk):
    announcement = get_object_or_404(Announcements, pk=pk)
    if announcement:
        announcement.views += 1
        announcement.save()
    serializer = AnnouncementSerializer(announcement,many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def event_detail(request,pk):
    event = get_object_or_404(Events, pk=pk)
    serializer = EventsSerializer(event,many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def checkin_detail(request,pk):
    checkin = get_object_or_404(CheckInToday, pk=pk)
    serializer = CheckInTodaySerializer(checkin,many=False)
    return Response(serializer.data)

@api_view(['GET', 'DELETE'])
@permission_classes([permissions.AllowAny])
def user_delete(request, pk):
    try:
        user = GGCUser.objects.get(pk=pk)
        user.delete()
    except GGCUser.DoesNotExist:
        return Http404
    return Response(status=status.HTTP_204_NO_CONTENT)