"""PR10: event admin, inlines, related object links and computed columns."""
from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from invitations_web.models import Invitation
from .models import Event


class EventInvitationInline(admin.TabularInline):
    model = Invitation
    extra = 0
    fields = ('guest', 'guest_name', 'response', 'status')
    autocomplete_fields = ('guest',)
    show_change_link = True
    verbose_name = 'Приглашение события'
    verbose_name_plural = 'Приглашения события'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date', 'user', 'name_length',
                    'invitation_count', 'site_link')
    list_display_links = ('id', 'name')
    list_filter = ('date', 'user')
    search_fields = ('name', 'user__name', 'user__email')
    ordering = ('-date', 'id')
    list_per_page = 15
    list_select_related = ('user',)
    autocomplete_fields = ('user',)
    readonly_fields = ('slug', 'name_length')
    inlines = (EventInvitationInline,)
    view_on_site = True

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _invitation_count=Count('invitations'))

    @admin.display(description='Приглашений', ordering='_invitation_count')
    def invitation_count(self, obj):
        return obj._invitation_count

    @admin.display(description='Страница на сайте')
    def site_link(self, obj):
        return format_html('<a href="{}">Открыть</a>', obj.get_absolute_url())
