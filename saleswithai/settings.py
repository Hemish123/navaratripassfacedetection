"""
Django settings for saleswithai project.
Navratri Face Pass Verification System.
"""
import os
from pathlib import Path

from decouple import config, Csv

# ──────────────────────────────────────────────
# BASE
# ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default="django-insecure-CHANGE-ME-in-production")
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*", cast=Csv())

_csrf = config("CSRF_TRUSTED_ORIGINS", default="")
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf.split(",") if o.strip()] if _csrf else []

# ──────────────────────────────────────────────
# APPS
# ──────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # ── project apps ──
    "generate_email",
    "users",
    "passes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "saleswithai.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "saleswithai.wsgi.application"

# ──────────────────────────────────────────────
# DATABASE
# ──────────────────────────────────────────────
import dj_database_url  # noqa: E402

_database_url = config("DATABASE_URL", default="")
if _database_url:
    DATABASES = {
        "default": dj_database_url.parse(
            _database_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ──────────────────────────────────────────────
# AUTH
# ──────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ──────────────────────────────────────────────
# I18N / TZ
# ──────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ──────────────────────────────────────────────
# STATIC FILES
# ──────────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ──────────────────────────────────────────────
# MEDIA (local fallback)
# ──────────────────────────────────────────────
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ──────────────────────────────────────────────
# AZURE BLOB STORAGE (optional)
# ──────────────────────────────────────────────
AZURE_STORAGE_CONNECTION_STRING = config("AZURE_STORAGE_CONNECTION_STRING", default="")
AZURE_STORAGE_ACCOUNT_NAME = config("AZURE_STORAGE_ACCOUNT_NAME", default="")
AZURE_STORAGE_ACCOUNT_KEY = config("AZURE_STORAGE_ACCOUNT_KEY", default="")
AZURE_STORAGE_CONTAINER = config("AZURE_STORAGE_CONTAINER", default="navratri-passes")
AZURE_SAS_EXPIRY_MINUTES = config("AZURE_SAS_EXPIRY_MINUTES", default=10, cast=int)

USE_AZURE_STORAGE = bool(AZURE_STORAGE_CONNECTION_STRING or AZURE_STORAGE_ACCOUNT_NAME)

# ──────────────────────────────────────────────
# CACHE
# ──────────────────────────────────────────────
_redis_url = config("REDIS_URL", default="")
if _redis_url:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": _redis_url,
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    }

# ──────────────────────────────────────────────
# FILE UPLOAD LIMITS
# ──────────────────────────────────────────────
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

# ──────────────────────────────────────────────
# FACE ENGINE
# ──────────────────────────────────────────────
FACE_MATCH_THRESHOLD = config("FACE_MATCH_THRESHOLD", default=0.45, cast=float)
FACE_REVIEW_THRESHOLD = config("FACE_REVIEW_THRESHOLD", default=0.35, cast=float)
FACE_MIN_DET_SCORE = config("FACE_MIN_DET_SCORE", default=0.6, cast=float)
FACE_MIN_FACE_SIZE = config("FACE_MIN_FACE_SIZE", default=80, cast=int)
FACE_BLUR_THRESHOLD = config("FACE_BLUR_THRESHOLD", default=50.0, cast=float)
FACE_MODEL_PACK = config("FACE_MODEL_PACK", default="buffalo_l")
FACE_USE_GPU = config("FACE_USE_GPU", default=False, cast=bool)

# ──────────────────────────────────────────────
# GATE
# ──────────────────────────────────────────────
GATE_KEY = config("GATE_KEY", default="change-me-in-production")
GATE_MAX_ENTRIES_PER_DAY = config("GATE_MAX_ENTRIES_PER_DAY", default=1, cast=int)

# ──────────────────────────────────────────────
# AZURE OPENAI (pass‑number OCR only)
# ──────────────────────────────────────────────
AZURE_OPENAI_ENDPOINT = config("AZURE_OPENAI_ENDPOINT", default="https://jivihireopenai.openai.azure.com")
AZURE_OPENAI_API_KEY = config("AZURE_OPENAI_KEY", default="")
AZURE_OPENAI_API_VERSION = config("AZURE_OPENAI_API_VERSION", default="2024-05-01-preview")
AZURE_OPENAI_DEPLOYMENT = config("AZURE_OPENAI_DEPLOYMENT", default="gpt-4o-mini")

# ──────────────────────────────────────────────
# SECURITY (production)
# ──────────────────────────────────────────────
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
    SECURE_HSTS_SECONDS = 31_536_000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# ──────────────────────────────────────────────
# MISC
# ──────────────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ──────────────────────────────────────────────
# LOGGING
# ──────────────────────────────────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "passes": {
            "handlers": ["console"],
            "level": config("LOG_LEVEL", default="INFO"),
            "propagate": True,
        },
    },
}
