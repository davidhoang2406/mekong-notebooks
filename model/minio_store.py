import io
import logging
import os

import fastavro
from minio import Minio

log = logging.getLogger(__name__)


def _build_client() -> Minio:
    endpoint = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
    secure   = endpoint.startswith("https://")
    host     = endpoint.split("://", 1)[-1]
    return Minio(
        host,
        access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
        secure=secure,
    )


class MinioStore:
    """Read-only MinIO wrapper for notebook use. Never writes to production buckets."""

    def __init__(self, bucket: str, client: Minio | None = None) -> None:
        self.bucket  = bucket
        self._client = client or _build_client()

    def list_objects(self, prefix: str = "", recursive: bool = True):
        return self._client.list_objects(self.bucket, prefix=prefix, recursive=recursive)

    def get_object(self, key: str):
        return self._client.get_object(self.bucket, key)

    def read_avro(self, key: str) -> list[dict]:
        response = self.get_object(key)
        try:
            return list(fastavro.reader(io.BytesIO(response.read())))
        finally:
            response.close()
            response.release_conn()
