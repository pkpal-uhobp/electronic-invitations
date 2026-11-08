from django.contrib import admin
from .models import Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest_name', 'event', 'status', 'response')
    list_filter = ('status', 'response')
    search_fields = ('guest_name', 'event__name')
    list_select_related = ('event', 'guest')
