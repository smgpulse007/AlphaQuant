from typing import Optional


class DocStore:
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket: str = "alpha-docs"):
        # TODO: init MinIO bucket
        self.bucket = bucket

    def put(self, key: str, data: bytes, content_type: Optional[str] = None) -> str:
        # TODO: upload object and return URL
        return f"minio://{self.bucket}/{key}"

