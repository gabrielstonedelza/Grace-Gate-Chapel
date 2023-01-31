from django.urls import path
from . import views

urlpatterns = [
    # all post requests
    path('add_member/', views.add_member),
    path('add_event/', views.add_event),
    path('add_announcement/', views.add_announcement),
    path('check_in/<str:phone_number>/', views.add_member_check_in),

    # all get requests
    path('all_members/', views.AllMembersView.as_view()),
    path('check_ins_today/', views.AllCheckInSTodayView.as_view()),
    path('events/', views.AllEventsView.as_view()),
    path('announcements/', views.AllAnnouncementsView.as_view()),

    # detail requests,update and delete
    path('member_detail/<int:pk>/', views.member_detail),
    path('member_update/<int:pk>/', views.update_member),
    path('member_delete/<int:pk>/', views.member_delete),
    path('approve_check_in/<int:pk>/', views.approve_check_in),
    path('my_check_in/<str:phone_number>/', views.get_my_check_ins),


]
