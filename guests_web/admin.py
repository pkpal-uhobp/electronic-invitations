"""Localized guest administration with linked invitations."""
from django.contrib import admin
from django.db.models import Count

from invitations_web.models import Invitation
from .models import Guest


class GuestInvitationInline(admin.TabularInline):
    model = Invitation
    extra = 0
    fields = ('event', 'guest_name', 'response', 'status')
    autocomplete_fields = ('event',)
    show_change_link = True
    verbose_name = 'Приглашение гостя'
    verbose_name_plural = 'Приглашения гостя'


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'invitation_count')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email')
    ordering = ('name', 'id')
    list_per_page = 15
    inlines = (GuestInvitationInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _invitation_count=Count('invitations'))

    @admin.display(description='Приглашений', ordering='_invitation_count')
    def invitation_count(self, obj):
        return obj._invitation_count
