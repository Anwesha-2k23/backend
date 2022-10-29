from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class ProfileImageStorage(S3Boto3Storage):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION1
    file_overwrite = False
    default_acl = 'public-read'

class StaticStorage(S3Boto3Storage):
    location = settings.AWS_STATIC_LOCATION
    default_acl = 'public-read'

class PublicQrStorage(S3Boto3Storage):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION2
    file_overwrite = False
    default_acl = 'public-read'

class PublicGalleryStorage(S3Boto3Storage):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION3
    file_overwrite = False
    default_acl = 'public-read'