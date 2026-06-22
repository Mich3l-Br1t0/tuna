"""Production settings — all secrets come from the environment."""

import os

from .base import *  # noqa: F403

DEBUG = False
ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

CORS_ALLOWED_ORIGINS = os.environ["CORS_ALLOWED_ORIGINS"].split(",")
CSRF_TRUSTED_ORIGINS = os.environ["CSRF_TRUSTED_ORIGINS"].split(",")

# HTTPS-only cookies in production
REST_AUTH = {**REST_AUTH, "JWT_AUTH_SECURE": True}  # noqa: F405

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
