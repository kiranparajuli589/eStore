from .base import *
from pathlib import Path

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += []

# EMAIL_CONFIGURATION
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"

PROJECT_ROOT = Path(__file__).parents[2]  # get root of the project
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")
MEDIA_URL = "/media/"
