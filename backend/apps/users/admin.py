from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from apps.users.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (*DjangoUserAdmin.list_display, "university")
    list_filter = (*DjangoUserAdmin.list_filter, "university")
    autocomplete_fields = ("university",)
    fieldsets = (
        *DjangoUserAdmin.fieldsets,
        ("University", {"fields": ("university",)}),
    )
