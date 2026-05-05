from .base import *  # noqa

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
        "CONN_MAX_AGE": 60,
        "OPTIONS": {
            # Neon requires SSL in production connections.
            "sslmode": config("DB_SSLMODE", default="require"),
        },
    }
}

# Free deployment mode:
# If Redis is unavailable, keep app running with local in-memory backends.
# Good for low-traffic demos/staging on free plans.
USE_REDIS = config("USE_REDIS", default=False, cast=bool)
if not USE_REDIS:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "elearn-prod-local-cache",
        }
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        }
    }
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
