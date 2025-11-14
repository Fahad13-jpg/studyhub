"""
Django settings for StudyGroupFinder project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qsl

import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# Load environment variables from .env file
load_dotenv()



# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------
# Secret Key & Debug
# ------------------------------------------------------------------
SECRET_KEY = os.getenv('SECRET_KEY', '_ojx++7g25ct5+73m$0t&&_+hlsam9tdy7q$#7#%0i69kf+1r&')
DEBUG = os.getenv('DEBUG', 'False') == 'False'

# ------------------------------------------------------------------
# Allowed Hosts
# ------------------------------------------------------------------
ALLOWED_HOSTS = [
    '.vercel.app', 
    '.now.sh', 
    'localhost', 
    '127.0.0.1',
    'study-group-finder-ousigqysn-fahad13-jpgs-projects.vercel.app'
]
CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'https://*.now.sh'
]
# ------------------------------------------------------------------
# Application definition
# ------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'crispy_forms',
    'crispy_bootstrap5',
    'cloudinary',
    'cloudinary_storage',

    # Your apps
    'accounts',
    'groups',
    'user_sessions',
    'dashboard',
    'chat',
    'recommendations',
    'notifications',
    'analytics',
    'gamification',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ------------------------------------------------------------------
# Authentication redirects
# ------------------------------------------------------------------
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'dashboard:dashboard'
LOGOUT_REDIRECT_URL = 'accounts:login'

# ------------------------------------------------------------------
# Middleware
# ------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ Serve static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'StudyGroupFinder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'StudyGroupFinder.wsgi.application'

# ------------------------------------------------------------------
# Database configuration
# ------------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    tmpPostgres = urlparse(DATABASE_URL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': tmpPostgres.path[1:],   # remove leading '/'
            'USER': tmpPostgres.username,
            'PASSWORD': tmpPostgres.password,
            'HOST': tmpPostgres.hostname,
            'PORT': tmpPostgres.port or 5432,
            'OPTIONS': dict(parse_qsl(tmpPostgres.query)),
        }
    }
else:
    # Fallback to local SQLite for development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ------------------------------------------------------------------
# Password Validation
# ------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ------------------------------------------------------------------
# Internationalization
# ------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------
# Static and Media files
# ------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ------------------------------------------------------------------
# Default Primary Key
# ------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Cloudinary Media Storage
