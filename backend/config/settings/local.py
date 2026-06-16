"""Local development settings."""

from config.settings.base import *  # noqa: F403

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
API_DOCS_ENABLED = True
