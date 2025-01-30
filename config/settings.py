

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-7gd#$!awnsyk!pwze=*r^53!5+irj%=o_2wdai!3dfaz1ze&3_'


DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'django_filters',

    'Authentication',
    'Attendance',
    'Survey',
    'WeeklySchedule',
    'Grades',
    'Blog',
    'corsheaders',
    
    
]
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]
CORS_ALLOW_HEADERS = [
    "Authorization",
    "Content-Type",
]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://localhost:\d+$",  # Allows any localhost port
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.save_response.SaveResponseMiddleware',
    'middleware.auto_refresh_jwt.AutoRefreshJWTMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'middleware.CustomJWTAuthentication.CustomJWTAuthentication'
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
        
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',  
        'rest_framework.throttling.UserRateThrottle',  
    ],
    'DEFAULT_THROTTLE_RATES': {
        'send_verification_code': '6/hour',  
        'anon': '10/minute',  
        'user': '1000/day', 
    },
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'Helli Scholl Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}


import os

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),  
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587 
EMAIL_USE_TLS = True  
EMAIL_HOST_USER = 'mahdiyar.mahdi31313@gmail.com' 
EMAIL_HOST_PASSWORD = 'lepv vlij oyig awjz'  
DEFAULT_FROM_EMAIL = 'mahdiyar.mahdi31313@gmail.com'  


AUTH_USER_MODEL = 'Authentication.UserBase'



from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=20), 
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7), 
    'ROTATE_REFRESH_TOKENS': True,    # محیط تست
    # 'ROTATE_REFRESH_TOKENS': False,  # تنظیمات برای جلوگیری از چرخش اتوماتیک توکن‌های Refresh
    # 'BLACKLIST_AFTER_ROTATION': True,  # وقتی که توکن‌ها چرخش پیدا می‌کنند، آن‌ها را به لیست سیاه اضافه کنید.
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,  
}




# SESSION_COOKIE_AGE = 60 * 60 * 24 * 7


# SESSION_COOKIE_SECURE = True  # برای استفاده در محیط‌های HTTPS


# # HttpOnly: اطمینان از اینکه کوکی‌ها توسط جاوا اسکریپت قابل دسترسی نیستند (جلوگیری از XSS)
# SESSION_COOKIE_HTTPONLY = True

# # SameSite: این ویژگی باعث جلوگیری از حملات CSRF می‌شود
# SESSION_COOKIE_SAMESITE = 'Strict'


# CSRF_COOKIE_SECURE = True


# CSRF_COOKIE_HTTPONLY = True
# CSRF_COOKIE_SAMESITE = 'Strict'

# # همچنین برای پشتیبانی از کوکی‌های امن در محیط‌های تولیدی، باید به این گزینه توجه کنید.
# SECURE_SSL_REDIRECT = True  # در صورتی که از HTTPS استفاده می‌کنید







# تنظیم کوکی‌ها
SESSION_COOKIE_SECURE = False  # در لوکال باید False باشد
CSRF_COOKIE_SECURE = False     # در لوکال باید False باشد
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 0        # در لوکال نباید HSTS فعال باشد
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_SSL_REDIRECT = False    # در لوکال نباید ریدایرکت به HTTPS شود
CORS_ALLOW_CREDENTIALS = True



# CORS_ORIGIN_ALLOW_ALL = False  # یا اینکه دامنه‌های مجاز را مشخص کنید
# CORS_ORIGIN_WHITELIST = [
#     'https://your-client-domain.com',  # دامنه‌ای که درخواست‌ها از آن ارسال می‌شود
# ]