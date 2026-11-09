"""PR10: invitation search, filters, relations, status editing and actions."""
from django.contrib import admin

from .models import Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest_name', 'event', 'organizer',
                    'event_date', 'status', 'response')
    list_display_links = ('id', 'guest_name')
    list_editable = ('status', 'response')
    list_filter = ('status', 'response', 'event__date', 'event')
    search_fields = ('guest_name', 'guest__email', 'event__name',
                     'event__user__name')
    ordering = ('-event__date', 'id')
    list_per_page = 15
    list_select_related = ('event', 'guest', 'event__user')
    autocomplete_fields = ('event', 'guest')

    @admin.display(description='Организатор', ordering='event__user__name')
    def organizer(self, obj):
        return obj.event.user.name if obj.event.user else 'Не указан'

    @admin.display(description='Дата события', ordering='event__date')
    def event_date(self, obj):
        return obj.event.date
