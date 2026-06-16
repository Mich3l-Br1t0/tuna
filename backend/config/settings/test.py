"""Test settings — self-contained so the suite runs without external services.

Required env vars are defaulted here (before base is imported) and the database is
swapped to in-memory SQLite, so ``pytest`` needs neither a ``.env`` file nor a running
PostgreSQL instance.
"""

import os

os.environ.setdefault("DJANGO_SECRET_KEY", "test-secret-key-not-for-production")
os.environ.setdefault("DATABASE_URL", "sqlite:////tmp/tuna_test.db")

from config.settings.base import *  # noqa: E402, F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Faster hashing keeps the suite snappy; never use MD5 outside tests.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Exercise the docs routes in tests (the schema-served smoke test depends on them).
API_DOCS_ENABLED = True
