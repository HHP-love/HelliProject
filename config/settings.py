


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

    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
        
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',  # برای کاربران ناشناس
        'rest_framework.throttling.UserRateThrottle',  # برای کاربران احراز هویت شده
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/minute',  # کاربران ناشناس تنها می‌توانند 10 درخواست در هر دقیقه ارسال کنند
        'user': '1000/day',  # کاربران احراز هویت شده تا 1000 درخواست در روز می‌توانند ارسال کنند
    }
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'Helli Scholl Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
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
            'filename': os.path.join(BASE_DIR, 'django.log'),  # مسیر فایل لاگ
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



# تنظیمات ارسال ایمیل
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587 
EMAIL_USE_TLS = True  
EMAIL_HOST_USER = 'mahdiyar.mahdi31313@gmail.com' 
EMAIL_HOST_PASSWORD = 'lepv vlij oyig awjz'  # رمز عبور ایمیل ارسال‌کننده

DEFAULT_FROM_EMAIL = 'mahdiyar.mahdi31313@gmail.com'  


AUTH_USER_MODEL = 'Authentication.UserBase'



from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # مدت زمان اعتبار توکن‌های Access
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # مدت زمان اعتبار توکن‌های Refresh
    'ROTATE_REFRESH_TOKENS': True,    # محیط تست
    # 'ROTATE_REFRESH_TOKENS': False,  # تنظیمات برای جلوگیری از چرخش اتوماتیک توکن‌های Refresh
    # 'BLACKLIST_AFTER_ROTATION': True,  # وقتی که توکن‌ها چرخش پیدا می‌کنند، آن‌ها را به لیست سیاه اضافه کنید.
    # 'ALGORITHM': 'HS256',  # الگوریتم رمزنگاری توکن
    # 'SIGNING_KEY': SECRET_KEY,  # کلید امضای JWT که باید مشابه کلید Django باشد
}




# SESSION_COOKIE_AGE = 60 * 60 * 72  

# # فقط کوکی‌های امن در HTTPS ارسال شوند
# # SESSION_COOKIE_SECURE = True  # برای استفاده در محیط‌های HTTPS
# SESSION_COOKIE_SECURE = False      #محیط تست

# # HttpOnly: اطمینان از اینکه کوکی‌ها توسط جاوا اسکریپت قابل دسترسی نیستند (جلوگیری از XSS)
# SESSION_COOKIE_HTTPONLY = True

# # SameSite: این ویژگی باعث جلوگیری از حملات CSRF می‌شود
# SESSION_COOKIE_SAMESITE = 'Strict'

# # این مورد برای کوکی‌های رفرش نیز صدق می‌کند، بنابراین باید در تنظیمات `CSRF_COOKIE_*` هم تنظیم شود.
# # CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = False      # محیط تست
# CSRF_COOKIE_HTTPONLY = True
# CSRF_COOKIE_SAMESITE = 'Strict'

# # همچنین برای پشتیبانی از کوکی‌های امن در محیط‌های تولیدی، باید به این گزینه توجه کنید.
# SECURE_SSL_REDIRECT = True  # در صورتی که از HTTPS استفاده می‌کنید
