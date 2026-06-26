from django.contrib import admin

from apps.events.models import EventData

from .models import Location, Stage


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "lanes")
    search_fields = ("name",)


class EventDataInline(admin.TabularInline):
    model = EventData
    extra = 1
    autocomplete_fields = ("event",)


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "date",
        "location",
        "registration_opens",
        "registration_deadline",
    )
    list_filter = ("date", "location")
    search_fields = ("name",)
    list_select_related = ("location",)
    inlines = [EventDataInline]
