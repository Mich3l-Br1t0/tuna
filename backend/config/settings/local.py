"""Local development settings."""

from config.settings.base import *  # noqa: F403

# Password-reset and other emails print to the console in development.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
