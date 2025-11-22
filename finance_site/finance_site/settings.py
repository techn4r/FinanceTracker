from pathlib import Path
import os

# Путь до корня проекта (там, где manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# !!! ВАЖНО !!!
# Для dev можно оставить как есть, но для боевого использования
# нужно сгенерировать свой секретный ключ.
SECRET_KEY = "django-insecure-change-me-in-production"

# В разработке=True, в проде обязательно False
DEBUG = False

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]


# Приложения проекта
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # наше приложение с трекером
    "finance",
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

ROOT_URLCONF = "finance_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # общая папка templates в корне (если захочешь использовать)
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,  # искать шаблоны внутри приложений (finance/templates/...)
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

WSGI_APPLICATION = "finance_site.wsgi.application"


# База данных
# Для простоты — SQLite. Для продакшена можно потом перейти на PostgreSQL.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Вариант под PostgreSQL (на будущее, закомментировано):
"""
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "finance_db",
        "USER": "postgres",
        "PASSWORD": "your-password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
"""

# Пароли (оставь по умолчанию)
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Локаль/таймзона

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Helsinki"  # можно сменить на Europe/Moscow, если нужно

USE_I18N = True
USE_TZ = True

# Статика
STATIC_URL = "static/"

# Дополнительно (если хочешь хранить свои статики в /static в корне проекта)
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Куда собирать статику при collectstatic (для продакшена)
STATIC_ROOT = BASE_DIR / "staticfiles"

# Медиа (если вдруг понадобится)
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Настройки входа/выхода
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"      # куда редиректить после логина
LOGOUT_REDIRECT_URL = "/"     # куда редиректить после логаута

# ID настроек (по умолчанию)
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
