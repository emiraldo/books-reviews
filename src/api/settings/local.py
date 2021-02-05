from .base import *

DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/static/'
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'


CELERY_BROKER_URL = f'redis://{os.environ["REDIS_HOST"]}:6379'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Bogota'
