from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Google Cloud Storage
if settings.GCP_STORAGE_ENABLED:
    from storages.backends.gcloud import GoogleCloudStorage

    class ProfileImageStorage(GoogleCloudStorage):
        def __init__(self, *args, **kwargs):
            kwargs['location'] = 'static/profile'
            super().__init__(*args, **kwargs)

    class StaticStorage(GoogleCloudStorage):
        def __init__(self, *args, **kwargs):
            kwargs['location'] = 'static'
            super().__init__(*args, **kwargs)

    class PublicQrStorage(GoogleCloudStorage):
        """GCS storage for QR codes with public read access"""
        def __init__(self, *args, **kwargs):
            kwargs['location'] = 'static/qr'
            super().__init__(*args, **kwargs)
        
        def _save(self, name, content):
            name = super()._save(name, content)
            # Make the file publicly readable
            self.bucket.blob(self.location + '/' + name).make_public()
            return name

    class PublicGalleryStorage(GoogleCloudStorage):
        def __init__(self, *args, **kwargs):
            kwargs['location'] = 'static/gallery'
            super().__init__(*args, **kwargs)

    class MultiCityStorage(GoogleCloudStorage):
        def __init__(self, *args, **kwargs):
            kwargs['location'] = 'static/multicity'
            super().__init__(*args, **kwargs)
    
    class PosterFileStorage(GoogleCloudStorage):
        """GCS storage for poster files with public read access"""
        def __init__(self, *args, **kwargs):
            kwargs['location'] = 'static/event_posters'
            super().__init__(*args, **kwargs)
        
        def _save(self, name, content):
            name = super()._save(name, content)
            # Make the file publicly readable
            self.bucket.blob(self.location + '/' + name).make_public()
            return name

# Only use S3 storage classes when S3 is enabled
elif settings.S3_ENABLED:
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
