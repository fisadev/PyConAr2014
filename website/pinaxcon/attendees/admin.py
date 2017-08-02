from django.contrib import admin

from .models import Attendee


class AttendeeAdmin(admin.ModelAdmin):
    search_fields = ('user__email', 'full_name')
    list_display = ('get_email', 'full_name')

    def get_email(self, object):
        return object.user.email

admin.site.register(Attendee, AttendeeAdmin)
