import os
import sys
from pathlib import Path

from django.urls import reverse_lazy

# Path(__file__) represents the full path to settings.py (CONDO_ME/src/project/settings.py.)
# Path(__file__).resolve().parent  ==> CONDO_ME/src/project/
# Path(__file__).resolve().parent.parent  ==> CONDO_ME/src/
# Path(__file__).resolve().parent.parent.parent  ==> CONDO_ME/
BASE_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

DATA_DIR = BASE_DIR / "data"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "change-me")

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True if os.environ.get("DEBUG") == "1" else False

ALLOWED_HOSTS = [
    h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()
]


# Application definition
# related to PYTHONPATH, in this case: /app/src/
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django_countries",
    "apps.prelogin",
    "apps.condo",
    # custom setup for condo_people in order to create groups and permissions
    "apps.condo_people.apps.CondoPeopleConfig",
    "apps.reservation",
    "apps.purchase",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

APPEND_SLASH = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "src" / "base_templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.condo_people.context_processors.user_groups",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}

# Changing Django standart user model to mine:
AUTH_USER_MODEL = "condo_people.User"


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },  # noqa: E501
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },  # noqa: E501
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },  # noqa: E501
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]  # noqa: E501


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# CSS, Media and JS files that WON'T CHANGE along time
STATIC_URL = "/static/"  # MUST BE STRING

# Path where Django sends collectstatic files
STATIC_ROOT = BASE_DIR / "data" / "web" / "static"

# used to specify additional directories for static files that are outside of apps
STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "src" / "base_static",
]

# URL available for users to access media files. MUST BE STRING
# it is NOT equivalent to a fisical folder. It's more like an URL.
MEDIA_URL = "/media/"  # i.e http://mysite.com/media/image.jpg

# where media files will be stored when transfered from.
MEDIA_ROOT = BASE_DIR / "data" / "web" / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# to @login_required
LOGIN_URL = reverse_lazy("apps.condo_people:login")

SITE_URL = "http://localhost:8000"
