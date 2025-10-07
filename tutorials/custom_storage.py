from storages.backends.s3boto3 import S3Boto3Storage

class CustomStorage(S3Boto3Storage):
    """
    Custom S3 storage class, for example, to modify file name or set custom ACLs.
    """
    # You can override any method or property here if necessary
    def __init__(self, *args, **kwargs):
        kwargs['bucket_name'] = 'code-with-sathya'  # Set your bucket name
        super().__init__(*args, **kwargs)
