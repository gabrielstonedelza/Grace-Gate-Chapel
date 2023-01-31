from django.urls import path
from . import views

urlpatterns = [
    path('add_member/', views.add_member),
    path('all_members/', views.AllMembersView.as_view()),
    path('check_ins_today/', views.AllCheckInSTodayView.as_view()),
    path('events/', views.AllEventsView.as_view()),
    path('announcements/', views.AllAnnouncementsView.as_view()),
    path('member_detail/<int:pk>/', views.member_detail),
    path('member_update/<int:id>/', views.update_member),
    path('member_delete/<int:id>/', views.member_delete),
    path('approve_check_in/<int:id>/', views.approve_check_in),
    path('my_check_in/<int:phone_number>/', views.get_my_check_ins),
    path('check_in/', views.add_member_check_in),
    path('add_event/', views.add_event),
    path('add_announcement/', views.add_announcement),
]