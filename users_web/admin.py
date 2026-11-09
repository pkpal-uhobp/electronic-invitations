"""Localized organizer administration and reverse event relations."""
from django.contrib import admin
from django.db.models import Count

from events_web.models import Event
from .models import User


class OrganizerEventInline(admin.TabularInline):
    model = Event
    extra = 0
    fields = ('name', 'date')
    show_change_link = True
    verbose_name = 'Событие организатора'
    verbose_name_plural = 'События организатора'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'event_count')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email')
    ordering = ('name', 'id')
    list_per_page = 15
    inlines = (OrganizerEventInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_event_count=Count('events'))

    @admin.display(description='Событий', ordering='_event_count')
    def event_count(self, obj):
        return obj._event_count
