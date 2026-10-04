import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'stellar-shipers-insecure-dev-key-change-in-production-2026!#*')

DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 'yes')

# Base allowed hosts from environment variable or standard defaults
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        'ALLOWED_HOSTS',
        'localhost,127.0.0.1,testserver,.onrender.com,.vercel.app,stellarshipers.com,www.stellarshipers.com'
    ).split(',')
    if host.strip()
]

# Guarantee production custom domains are always permitted
PRODUCTION_DOMAINS = [
    'stellarshipers.com',
    'www.stellarshipers.com',
]
for domain in PRODUCTION_DOMAINS:
    if domain not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(domain)

# Automatic Render deployment host detection
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Automatic Vercel deployment host detection
VERCEL_URL = os.getenv('VERCEL_URL')
if VERCEL_URL and VERCEL_URL not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(VERCEL_URL)

# CSRF Trusted Origins for HTTPS on Render, Vercel & Production Custom Domain
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        'CSRF_TRUSTED_ORIGINS',
        'https://*.onrender.com,https://*.vercel.app,http://localhost:8000,http://127.0.0.1:8000,https://stellarshipers.com,https://www.stellarshipers.com'
    ).split(',')
    if origin.strip()
]

PRODUCTION_CSRF_ORIGINS = [
    'https://stellarshipers.com',
    'https://www.stellarshipers.com',
]
for origin in PRODUCTION_CSRF_ORIGINS:
    if origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(origin)

if RENDER_EXTERNAL_HOSTNAME:
    render_origin = f'https://{RENDER_EXTERNAL_HOSTNAME}'
    if render_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(render_origin)

if VERCEL_URL:
    vercel_origin = f'https://{VERCEL_URL}'
    if vercel_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(vercel_origin)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    # Custom B2B Apps
    'apps.core.apps.CoreConfig',
    'apps.products.apps.ProductsConfig',
    'apps.rfq.apps.RfqConfig',
    'apps.pages.apps.PagesConfig',
    'apps.dashboard.apps.DashboardConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'stellar_shipers.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'stellar_shipers.wsgi.application'

# Database Configuration
# Default to self-contained SQLite (No external database required for Render)
# Automatically enables PostgreSQL if DATABASE_URL is optionally provided (Supabase, Neon, etc.)
DATABASE_URL = os.getenv('DATABASE_URL')
IS_VERCEL = os.getenv('VERCEL') == '1'

def get_sqlite_path():
    db_file = BASE_DIR / 'db.sqlite3'
    if IS_VERCEL:
        import shutil
        tmp_db = '/tmp/db.sqlite3'
        if not os.path.exists(tmp_db) and os.path.exists(db_file):
            shutil.copy2(db_file, tmp_db)
        return tmp_db
    return db_file

if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.parse(
                DATABASE_URL,
                conn_max_age=0 if IS_VERCEL else 600,
                ssl_require=True
            )
        }
    except Exception:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': get_sqlite_path(),
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': get_sqlite_path(),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (User uploads, Technical Spec sheets, Product photos)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Storage Configuration (Supabase Storage S3-compatible backend / Local FileSystem fallback)
USE_SUPABASE_STORAGE = bool(
    os.getenv('SUPABASE_STORAGE_ACCESS_KEY') and
    os.getenv('SUPABASE_STORAGE_BUCKET')
)

if USE_SUPABASE_STORAGE:
    endpoint_url = os.getenv("SUPABASE_STORAGE_ENDPOINT")  # e.g., https://<project-ref>.supabase.co/storage/v1/s3
    bucket_name = os.getenv("SUPABASE_STORAGE_BUCKET", "stellar-media")
    region_name = os.getenv("SUPABASE_STORAGE_REGION", "ap-south-1")

    # Derive public Supabase CDN domain for direct, unauthenticated client downloads
    from urllib.parse import urlparse
    parsed_endpoint = urlparse(endpoint_url) if endpoint_url else None
    custom_domain = f"{parsed_endpoint.netloc}/storage/v1/object/public/{bucket_name}" if parsed_endpoint and parsed_endpoint.netloc else None

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "access_key": os.getenv("SUPABASE_STORAGE_ACCESS_KEY"),
                "secret_key": os.getenv("SUPABASE_STORAGE_SECRET_KEY"),
                "bucket_name": bucket_name,
                "endpoint_url": endpoint_url,
                "custom_domain": custom_domain,
                "region_name": region_name,
                "default_acl": None,
                "file_overwrite": False,
                "querystring_auth": False,
            },
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        },
    }
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        },
    }

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Configuration
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'STELLAR SHIPERS <contact@stellarshipers.com>')
ADMIN_NOTIFICATION_EMAIL = os.getenv('ADMIN_NOTIFICATION_EMAIL', 'contact@stellarshipers.com')

# Security Headers (Production-ready toggles)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True').lower() in ('true', '1', 'yes')
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_CONTENT_TYPE_NOSNIFF = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
