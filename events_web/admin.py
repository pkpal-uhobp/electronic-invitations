from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date', 'user')
    list_filter = ('date',)
    search_fields = ('name', 'user__name')
