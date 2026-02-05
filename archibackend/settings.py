from pathlib import Path
import dj_database_url
from datetime import timedelta
import os


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = [
    "archi-reflex-backend.onrender.com",
    "https://archi-reflex.com",
    "https://admin.archi-reflex.com",
    "localhost",
    "127.0.0.1",
]




INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    'drf_yasg',

    "corsheaders",


    'rest_framework',

    'appointments',
    'internships',
    'projects',
    'contacts',
    'core',

    'cloudinary',
    'cloudinary_storage',
]



SECURE_SSL_REDIRECT = True

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


CSRF_TRUSTED_ORIGINS = [
    "https://archi-reflex-front-site.vercel.app",
    "https://archi-reflex-front-admin.vercel.app",
    "https://archi-reflex.com",
    "https://admin.archi-reflex.com",
]

CORS_ALLOW_CREDENTIALS = True



CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://archi-reflex-front-site.vercel.app",
    "https://archi-reflex-front-admin.vercel.app",
    "https://archi-reflex-frontend.onrender.com",
    "https://archi-reflex.com",
    "https://admin.archi-reflex.com",
]



CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'



MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "archibackend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]



CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv("CLOUDINARY_CLOUD_NAME"),
    'API_KEY': os.getenv("CLOUDINARY_API_KEY"),
    'API_SECRET': os.getenv("CLOUDINARY_API_SECRET"),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'



WSGI_APPLICATION = "archibackend.wsgi.application"



DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}



ADMIN_EMAIL = 'eboctholi@archi-reflex.com'



GOOGLE_CREDENTIALS_FILE = BASE_DIR / 'service_account.json'
GOOGLE_TIMEZONE = 'Africa/Lome'
GOOGLE_CALENDAR_ID = "a8e12f026d3d4bfed797fba69c09570966733beafe92f662490bb4b62de7644b@group.calendar.google.com"



SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30*6),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30*6),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
}


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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Lome"


USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = "static/"
