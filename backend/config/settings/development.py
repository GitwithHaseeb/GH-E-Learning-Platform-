import os  # noqa: E402

from .base import *  # noqa

DEBUG = True
ALLOWED_HOSTS = ["*"]
SECURE_SSL_REDIRECT = False

# Debug toolbar optional — URL checks ke saath kabhi kabhi conflict; zarurat ho to enable karein
if os.environ.get("ENABLE_DEBUG_TOOLBAR", "").lower() in ("1", "true", "yes"):
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ["127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="elearning"),
        "USER": config("DB_USER", default="postgres"),
        "PASSWORD": config("DB_PASSWORD", default="postgres"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

# Agar PostgreSQL available na ho to SQLite fallback (sirf local demo)
if os.environ.get("USE_SQLITE", "").lower() in ("1", "true", "yes"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Local dev: bina real email server ke signup test karne ke liye
ACCOUNT_EMAIL_VERIFICATION = "none"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Redis install/run na ho to bhi `runserver` chale — throttling + sessions LocMem par.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.db"
CHANNEL_LAYERS = {
    "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"},
}
