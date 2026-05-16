from .base import *

DEBUG = False

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default=".karyawijaya.com",
).split(",")

CORS_ALLOW_ALL_ORIGINS = False