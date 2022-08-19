import os
from .common import *


# Password validation

AUTH_PASSWORD_VALIDATORS = []


# Email settings

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'tmp/mailbox')
