from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from apps.users import services
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
    actions = ("send_password_setup_email",)

    @admin.action(description="Send password setup email")
    def send_password_setup_email(self, request, queryset):
        sent = 0
        for user in queryset:
            if user.email:
                services.send_password_setup_email(user, request=request)
                sent += 1
        self.message_user(request, f"Sent {sent} password setup email(s).")
