from django.contrib import admin

from apps.universities.models import Athlete, University


class AthleteInline(admin.TabularInline):
    model = Athlete
    extra = 0


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ("name", "normalized_name", "created_at")
    search_fields = ("name", "normalized_name")
    readonly_fields = ("normalized_name",)
    inlines = (AthleteInline,)


@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ("name", "university")
    list_filter = ("university",)
    search_fields = ("name",)
    autocomplete_fields = ("university",)
