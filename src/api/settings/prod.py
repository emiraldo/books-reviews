from .base import *

DEBUG = False

CORS_ORIGIN_ALLOW_ALL = True

ALLOWED_HOSTS = [
    "13.58.116.139",
    "localhost",
    "127.0.0.1"
]

CELERY_BROKER_URL = f'redis://{os.environ["REDIS_HOST"]}:6379'

CELERY_TIMEZONE = 'America/Bogota'

CELERY_RESULT_BACKEND = 'django-db'
