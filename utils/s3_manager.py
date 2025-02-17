# utils/s3_manager.py
import boto3
import json
from pathlib import Path
from typing import Union, BinaryIO
from utils.config import config

class S3Manager:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            region_name=config.AWS_REGION
        )
        self.bucket_name = config.S3_BUCKET_NAME
    
    def upload_file(self, file_path: Union[str, Path], s3_key: str) -> bool:
        """Upload a file to S3."""
        try:
            self.s3_client.upload_file(str(file_path), self.bucket_name, s3_key)
            return True
        except Exception as e:
            print(f"Error uploading file to S3: {e}")
            return False
    
    def upload_fileobj(self, file_obj: BinaryIO, s3_key: str) -> bool:
        """Upload a file object to S3."""
        try:
            self.s3_client.upload_fileobj(file_obj, self.bucket_name, s3_key)
            return True
        except Exception as e:
            print(f"Error uploading file object to S3: {e}")
            return False
    
    def download_file(self, s3_key: str, local_path: Union[str, Path]) -> bool:
        """Download a file from S3."""
        try:
            self.s3_client.download_file(self.bucket_name, s3_key, str(local_path))
            return True
        except Exception as e:
            print(f"Error downloading file from S3: {e}")
            return False
    
    def list_files(self, prefix: str = "") -> list:
        """List files in S3 bucket with given prefix."""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            return [obj['Key'] for obj in response.get('Contents', [])]
        except Exception as e:
            print(f"Error listing files in S3: {e}")
            return []