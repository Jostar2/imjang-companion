from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from services.api.app.core.config import repo_root, settings


@dataclass(slots=True)
class StoredAttachment:
    storage_backend: str
    storage_key: str
    size_bytes: int


class LocalStorageService:
    def save_bytes(self, visit_id: str, attachment_id: str, filename: str, content: bytes) -> StoredAttachment:
        upload_root = repo_root / settings.upload_root / visit_id
        upload_root.mkdir(parents=True, exist_ok=True)

        safe_name = Path(filename or "upload.bin").name.replace(" ", "-")
        storage_key = Path(settings.upload_root) / visit_id / f"{attachment_id}-{safe_name}"
        destination = repo_root / storage_key
        destination.write_bytes(content)

        return StoredAttachment(
            storage_backend="local",
            storage_key=str(storage_key).replace("\\", "/"),
            size_bytes=len(content),
        )

    def delete(self, storage_key: str) -> None:
        if not storage_key:
            return
        file_path = repo_root / storage_key
        if file_path.is_file():
            file_path.unlink()


class S3CompatibleStorageService:
    def __init__(self) -> None:
        import boto3

        self._client = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region,
        )

    def save_bytes(self, visit_id: str, attachment_id: str, filename: str, content: bytes) -> StoredAttachment:
        safe_name = Path(filename or "upload.bin").name.replace(" ", "-")
        storage_key = f"visits/{visit_id}/{attachment_id}-{safe_name}"
        self._client.put_object(Bucket=settings.s3_bucket, Key=storage_key, Body=content)
        return StoredAttachment(storage_backend="s3", storage_key=storage_key, size_bytes=len(content))

    def delete(self, storage_key: str) -> None:
        if not storage_key:
            return
        self._client.delete_object(Bucket=settings.s3_bucket, Key=storage_key)


def get_storage_service() -> LocalStorageService | S3CompatibleStorageService:
    if settings.storage_backend == "s3":
        return S3CompatibleStorageService()
    return LocalStorageService()


storage_service = get_storage_service()
