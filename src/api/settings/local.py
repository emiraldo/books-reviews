from .base import *

DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/static/'
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'


CELERY_BROKER_URL = f'redis://{os.environ["REDIS_HOST"]}:6379'

CELERY_TIMEZONE = 'America/Bogota'

CELERY_RESULT_BACKEND = 'django-db'