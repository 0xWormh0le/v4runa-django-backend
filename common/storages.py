from storages.backends.s3boto3 import S3Boto3Storage
from storages.backends.gcloud import GoogleCloudStorage


class PublicStorage(GoogleCloudStorage):
    default_acl = 'public-read'
    location = 'public'


class PrivateStorage(GoogleCloudStorage):
    default_acl = 'private'
    location = 'private'
