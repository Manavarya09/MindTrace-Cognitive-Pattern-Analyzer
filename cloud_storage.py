# MindTrace - Cloud Storage Module

"""
AWS S3 and Google Cloud Storage integration
"""

import boto3
from google.cloud import storage

class CloudStorage:
    """Multi-cloud storage abstraction"""
    
    def __init__(self, provider='local'):
        self.provider = provider
        self.client = None
        
        if provider == 's3':
            try:
                self.client = boto3.client('s3')
            except:
                pass
        elif provider == 'gcs':
            try:
                self.client = storage.Client()
            except:
                pass
    
    def upload_file(self, local_path, bucket, remote_path):
        if self.provider == 's3' and self.client:
            self.client.upload_file(local_path, bucket, remote_path)
            return f"s3://{bucket}/{remote_path}"
        elif self.provider == 'gcs' and self.client:
            bucket = self.client.bucket(bucket)
            blob = bucket.blob(remote_path)
            blob.upload_from_filename(local_path)
            return f"gs://{bucket}/{remote_path}"
        
        return None
    
    def download_file(self, bucket, remote_path, local_path):
        if self.provider == 's3' and self.client:
            self.client.download_file(bucket, remote_path, local_path)
        elif self.provider == 'gcs' and self.client:
            bucket = self.client.bucket(bucket)
            blob = bucket.blob(remote_path)
            blob.download_to_filename(local_path)
    
    def list_files(self, bucket, prefix=''):
        if self.provider == 's3' and self.client:
            response = self.client.list_objects_v2(Bucket=bucket, Prefix=prefix)
            return [obj['Key'] for obj in response.get('Contents', [])]
        
        return []

cloud_storage = CloudStorage('local')
print("Cloud storage module ready!")
