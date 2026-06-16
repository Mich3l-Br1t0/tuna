"""Write-side operations for user accounts (HackSoft services layer)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.forms import PasswordResetForm
from django.db import transaction

from apps.users.models import User

if TYPE_CHECKING:
    from django.http import HttpRequest

    from apps.universities.models import University


class _InvitePasswordResetForm(PasswordResetForm):
    """Password-reset form that also targets accounts without a usable password.

    Django's default ``get_users`` filters out accounts with unusable passwords, which
    would exclude freshly invited university accounts. We keep their password unusable
    until they set one via the emailed link, so we override the filter to include them.
    """

    def get_users(self, email: str):
        email_field = User.get_email_field_name()
        active_users = User._default_manager.filter(
            **{f"{email_field}__iexact": email, "is_active": True}
        )
        return (
            user
            for user in active_users
            if getattr(user, email_field).casefold() == email.casefold()
        )


def send_password_setup_email(user: User, *, request: HttpRequest | None = None) -> None:
    """Email ``user`` a password set/reset link using Django's reset machinery.

    Works both from the admin (pass ``request`` so the link host derives from it) and
    headless (falls back to a local domain — refined once the frontend URL is known).
    """
    form = _InvitePasswordResetForm({"email": user.email})
    if not form.is_valid():
        return

    opts: dict = {"use_https": bool(request and request.is_secure())}
    if request is not None:
        opts["request"] = request
    else:
        opts["domain_override"] = "localhost:8000"

    form.save(**opts)


@transaction.atomic
def create_university_account(
    *,
    username: str,
    email: str,
    university: University,
    request: HttpRequest | None = None,
) -> User:
    """Create a university's login account and email it a password-setup link.

    The account starts with an unusable password; the university establishes one
    through the emailed link (the same flow as ``/api/auth/password/reset/``).
    """
    user = User(username=username, email=email, university=university, is_staff=False)
    user.set_unusable_password()
    user.full_clean()
    user.save()

    send_password_setup_email(user, request=request)
    return user
