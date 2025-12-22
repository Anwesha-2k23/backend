from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Only use S3 storage classes when S3 is enabled
if settings.S3_ENABLED:
    from storages.backends.s3boto3 import S3Boto3Storage

    class ProfileImageStorage(S3Boto3Storage):
        location = settings.AWS_PUBLIC_MEDIA_LOCATION1
        file_overwrite = False
        default_acl = "public-read"

    class StaticStorage(S3Boto3Storage):
        location = settings.AWS_STATIC_LOCATION
        default_acl = "public-read"

    class PublicQrStorage(S3Boto3Storage):
        location = settings.AWS_PUBLIC_MEDIA_LOCATION2
        file_overwrite = False
        default_acl = "public-read"

    class PublicGalleryStorage(S3Boto3Storage):
        location = settings.AWS_PUBLIC_MEDIA_LOCATION3
        file_overwrite = False
        default_acl = "public-read"

    class MultiCityStorage(S3Boto3Storage):
        location = settings.AWS_PUBLIC_MEDIA_LOCATION4
        file_overwrite = False
        default_acl = "public-read"
else:
    # Use FileSystemStorage for local development, with base_url for proper .url generation
    class ProfileImageStorage(FileSystemStorage):
        def __init__(self, *args, **kwargs):
            kwargs['location'] = 'static/profile'
            kwargs['base_url'] = settings.STATIC_URL
            super().__init__(*args, **kwargs)
    
    class StaticStorage(FileSystemStorage):
        def __init__(self, *args, **kwargs):
            kwargs['location'] = 'static'
            kwargs['base_url'] = settings.STATIC_URL
            super().__init__(*args, **kwargs)
    
    class PublicQrStorage(FileSystemStorage):
        def __init__(self, *args, **kwargs):
            kwargs['location'] = 'static/qr'
            kwargs['base_url'] = settings.STATIC_URL
            super().__init__(*args, **kwargs)
    
    class PublicGalleryStorage(FileSystemStorage):
        def __init__(self, *args, **kwargs):
            kwargs['location'] = 'static/gallery'
            kwargs['base_url'] = settings.STATIC_URL
            super().__init__(*args, **kwargs)
    
    class MultiCityStorage(FileSystemStorage):
        def __init__(self, *args, **kwargs):
            kwargs['location'] = 'static/multicity'
            kwargs['base_url'] = settings.STATIC_URL
            super().__init__(*args, **kwargs)
