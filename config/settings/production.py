from .base import *

DEBUG = False

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default=".karyawijaya.com,.portal.kawi-nickel.com",
).split(",")

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "https://apps.portal.kawi-nickel.com",
    "https://karyawijaya.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://apps.portal.kawi-nickel.com",
    "https://karyawijaya.com",
]