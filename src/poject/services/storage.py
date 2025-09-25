import os
from typing import List
import boto3
from botocore.exceptions import ClientError
from ..config.settings import settings
from ..utils.logger import logger

class S3Storage:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        self.bucket = settings.S3_BUCKET

    def list_objects(self, prefix: str = "") -> List[str]:
        """List all objects under prefix"""
        keys = []
        paginator = self.s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                keys.append(obj["Key"])
        logger.info("Found %d objects in bucket '%s' with prefix '%s'", len(keys), self.bucket, prefix)
        return keys

    def download_file(self, key: str, dest_path: str) -> None:
        """Upload files from s3"""
        dir_path = os.path.dirname(dest_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        try:
            logger.info("Downloading s3://%s/%s -> %s", self.bucket, key, dest_path)
            self.s3.download_file(self.bucket, key, dest_path)
        except ClientError as e:
            logger.error("S3 download error: %s", e)
            raise

    def download_folder(self, prefix: str, local_dir: str) -> None:
        """upload all files under prefix with the same structure"""
        keys = self.list_objects(prefix)
        for key in keys:
            if key.endswith("/"):
                continue  # ignorer les dossiers virtuels
            # garder la structure relative du prefix
            relative_path = os.path.relpath(key, prefix)
            local_path = os.path.join(local_dir, relative_path)
            self.download_file(key, local_path)
