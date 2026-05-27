import logging
import boto3
from fastapi import HTTPException
from botocore.exceptions import ClientError, BotoCoreError
from fastapi.concurrency import run_in_threadpool

from edulafia.config import settings

logger = logging.getLogger(__name__)


def _get_s3_client():
    aws_key = settings.AWS_ACCESS_KEY_ID
    aws_secret = settings.AWS_SECRET_ACCESS_KEY
    aws_region = settings.AWS_REGION
    aws_bucket = settings.AWS_S3_BUCKET

    if not all([aws_key, aws_secret, aws_bucket]):
        raise HTTPException(
            status_code=500,
            detail="S3 Cloud Storage is not fully configured."
        )
    return boto3.client(
        "s3",
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret,
        region_name=aws_region,
    )


class S3StorageClient:
    """Async wrapper for Boto3 S3 operations."""

    @classmethod
    async def upload_file(cls, file_bytes: bytes, file_key: str, content_type: str) -> str:
        """Upload a file to S3 and return its public URL."""
        s3 = _get_s3_client()
        aws_bucket = settings.AWS_S3_BUCKET
        aws_region = settings.AWS_REGION
        try:
            await run_in_threadpool(
                s3.put_object,
                Bucket=aws_bucket,
                Key=file_key,
                Body=file_bytes,
                ContentType=content_type,
            )
            return f"https://{aws_bucket}.s3.{aws_region}.amazonaws.com/{file_key}"
        except (ClientError, BotoCoreError) as e:
            logger.error(f"S3 Upload failed: {e}")
            raise HTTPException(status_code=502, detail="File upload to cloud storage failed due to network or configuration issue.")

    @classmethod
    async def delete_file(cls, file_key: str) -> bool:
        """Delete a file from S3."""
        s3 = _get_s3_client()
        aws_bucket = settings.AWS_S3_BUCKET
        try:
            await run_in_threadpool(
                s3.delete_object,
                Bucket=aws_bucket,
                Key=file_key
            )
            return True
        except (ClientError, BotoCoreError) as e:
            logger.error(f"S3 Deletion failed: {e}")
            return False