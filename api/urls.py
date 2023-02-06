from django.urls import path
from . import views

urlpatterns = [
    # all post requests
    # path('add_member/', views.add_member),
    path('add_event/', views.add_event),
    path('add_announcement/', views.add_announcement),
    path('add_devotion/', views.add_devotion),
    path('check_in/', views.add_member_check_in),

    # all get requests
    # path('all_members/', views.AllMembersView.as_view()),
    path('check_ins_today/', views.AllCheckInSTodayView.as_view()),
    path('events/', views.AllEventsView.as_view()),
    path('announcements/', views.AllAnnouncementsView.as_view()),
    path('devotions/', views.AllDevotionView.as_view()),

    # detail requests,update and delete
    # path('member_detail/<int:pk>/', views.member_detail),
    path('devotion_detail/<int:pk>/', views.devotion_detail),
    path('announcement_detail/<int:pk>/', views.announcement_detail),
    path('event_detail/<int:pk>/', views.event_detail),
    path('checkin_detail/<int:pk>/', views.checkin_detail),
    # path('member_update/<int:pk>/', views.update_member),
    # path('member_delete/<int:pk>/', views.member_delete),
    path('approve_check_in/<int:pk>/', views.approve_check_in),
    path('my_check_in/', views.get_my_check_ins),
    path("delete_user/<int:pk>/", views.user_delete),
    #     notifications
    path('my_notifications/', views.get_all_user_notifications),
    path('get_user_unread_notifications/', views.get_user_unread_notifications),
    path('get_triggered_notifications/', views.get_triggered_notifications),
    path('read_notification/', views.read_notification)


]
