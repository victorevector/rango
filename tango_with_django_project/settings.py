"""
Django settings for tango_with_django_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates') #pathway to Template/ directory

STATIC_PATH = os.path.join(BASE_DIR,'static') #pathyway to Static/ directory


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e0wsh%zp&jp7=xhsg0^ad=#ttvrxy3&zw0rtxt380*4x-f*6m-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rango',
    'registration',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tango_with_django_project.urls'

WSGI_APPLICATION = 'tango_with_django_project.wsgi.application'

# Templates

TEMPLATE_DIRS = [
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    TEMPLATE_PATH,
    ]


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    STATIC_PATH,
    )

# Media files

MEDIA_URL = '/media/' #user uploaded files will be availbe from http://.../media/
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') #tells Django where uploaded files should be stored on local disk

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher', ##default##
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    )

LOGIN_URL = '/accounts/login/'

# Registration Redux
REGISTRATION_OPEN = True
ACCOUNT_ACTIVATION_DAYS = 7 #one week activation window
REGISTRATION_AUTO_LOGIN = True #user will be automatically logged in 
LOGIN_REDIRECT_URL = '/rango/' #the page you want users to arrive at after they succesfully log in
LOGIN_URL = '/accounts/login/' #users get redirected to this page if they try to access pages that required authentication and they are not logged in

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'