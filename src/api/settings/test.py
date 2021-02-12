from .base import * # noqa

IS_TESTING = True

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES = True
