import os
from pathlib import Path


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# ENVIRONMENT CONFIGURATION
# ============================================================

def config(var, default=None):
    return os.environ.get(var, default)


def config_bool(var, default=False):
    value = os.environ.get(var)

    if value is None:
        return default

    return value.lower() in ("true", "1", "yes", "on")


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = config(
    "SECRET_KEY",
    "django-insecure-change-this-in-production"
)

DEBUG = config_bool("DEBUG", default=True)

ALLOWED_HOSTS = [
    host.strip()
    for host in config(
        "ALLOWED_HOSTS",
        "localhost,127.0.0.1"
    ).split(",")
    if host.strip()
]


# ============================================================
# APPLICATION DEFINITION
# ============================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sitemaps",
    "django.contrib.sites",

    "crispy_forms",
    "crispy_bootstrap5",
    "widget_tweaks",

    "blog",
]

SITE_ID = 1


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise for serving static files in production
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "blog.middleware.ActiveUserMiddleware",
]


# ============================================================
# URL CONFIGURATION
# ============================================================

ROOT_URLCONF = "blogproject.urls"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                "blog.context_processors.base_context",
            ],
        },
    },
]


# ============================================================
# WSGI
# ============================================================

WSGI_APPLICATION = "blogproject.wsgi.application"


# ============================================================
# DATABASE
# ============================================================
#
# Currently keeping SQLite for your local/development setup.
# Later, we will configure PostgreSQL for Render production.
#

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# WhiteNoise static file storage
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },

    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ============================================================
# MEDIA FILES
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================
# LOGIN / LOGOUT
# ============================================================

LOGIN_URL = "blog:login"

LOGIN_REDIRECT_URL = "blog:home"

LOGOUT_REDIRECT_URL = "blog:home"


# ============================================================
# CRISPY FORMS
# ============================================================

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"


# ============================================================
# TINYMCE CONFIGURATION
# ============================================================

TINYMCE_DEFAULT_CONFIG = {
    "height": 500,
    "width": "100%",

    "cleanup_on_startup": True,

    "custom_undo_redo_levels": 20,

    "selector": "textarea",

    "plugins": (
        "textcolor save link image media preview codesample "
        "contextmenu table code lists fullscreen insertdatetime "
        "nonbreaking contextmenu directionality searchreplace "
        "wordcount visualblocks visualchars code fullscreen "
        "autolink lists charmap print hr anchor pagebreak"
    ),

    "toolbar1": (
        "fullscreen preview bold italic underline | "
        "fontselect, fontsizeselect | "
        "forecolor backcolor | "
        "alignleft alignright | "
        "aligncenter alignjustify | "
        "indent outdent | "
        "bullist numlist table | "
        "link image media | "
        "codesample |"
    ),

    "toolbar2": (
        "visualblocks visualchars | "
        "charmap hr pagebreak nonbreaking anchor | "
        "code | "
        "undo redo | "
        "cut copy paste | "
        "searchreplace | "
        "wordcount |"
    ),

    "contextmenu": "formats | link image",

    "menubar": True,

    "statusbar": True,
}


# ============================================================
# EMAIL
# ============================================================

# Development/testing email backend
# No real emails are sent.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# ============================================================
# BASE URL
# ============================================================

BASE_URL = config(
    "BASE_URL",
    "http://localhost:8000"
)


# ============================================================
# CACHE
# ============================================================

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
        "TIMEOUT": 300,
    }
}


# ============================================================
# PRODUCTION SECURITY
# ============================================================

if not DEBUG:

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    X_FRAME_OPTIONS = "DENY"

    SECURE_HSTS_SECONDS = 31536000

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_HSTS_PRELOAD = True