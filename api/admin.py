from django.contrib import admin

from .models import AddMember, CheckInToday, Announcements, Events, MorningDevotion, Notifications


admin.site.register(AddMember)
admin.site.register(CheckInToday)
admin.site.register(Announcements)
admin.site.register(Events)
admin.site.register(MorningDevotion)
admin.site.register(Notifications)