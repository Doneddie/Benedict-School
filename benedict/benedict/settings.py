"""
Django settings for benedict project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-@dy&%7$qjzu+8nooddcv%b7d-4e0gz)swt*^5_%p&ah-3$618q"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "benedict_school",
    "bootstrap4",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "crispy_forms",
    "debug_toolbar",
    "corsheaders",
    "storages",
    "widget_tweaks",
    "rest_framework", 
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "benedict.urls"

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
                  # ... other context processors ...
                "benedict_school.context_processors.google_maps_api_key",
            ],
        },
    },
]

WSGI_APPLICATION = "benedict.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "benedict_school/static", 
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = '/media/'  # This is the public URL to access uploaded files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # This is the path where files will be stored

# Email backend settings (for development, using the console backend)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # For example, using Gmail's SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "julia07n@yahoo.com"  # Your email address for sending emails
EMAIL_HOST_PASSWORD = 'your_email_password'  # Your email password (or app-specific password)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Use the email you send from as the default sender address


CONTACT_EMAIL = "julia07n@yahoo.com"

# Add trusted origins for CSRF protection
CSRF_TRUSTED_ORIGINS = [
    'https://localhost:8000',  # Added localhost URL (use http://localhost if not using HTTPS)
    'http://localhost:8000',   # Add for HTTP if not using HTTPS
    'http://127.0.0.1:8000',   # Using the 127.0.0.1 IP address
]

LOGIN_REDIRECT_URL = '/admin-dashboard/'  # Redirect admins after login
LOGOUT_REDIRECT_URL = '/admin-login/'     # Redirect to login page after logout


