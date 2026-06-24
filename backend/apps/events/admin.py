from django.contrib import admin

from .models import Event, EventCategory


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "type")
    list_filter = ("type",)
    search_fields = ("name",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "measurement_type")
    list_filter = ("category", "measurement_type")
    search_fields = ("name",)
    list_select_related = ("category",)
