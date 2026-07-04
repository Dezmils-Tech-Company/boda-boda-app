from io import BytesIO
from typing import Any, Optional
from uuid import uuid4

try:
    import cloudinary
    import cloudinary.uploader
except ImportError:  # pragma: no cover - depends on environment
    cloudinary = None
    cloudinary_uploader = None

from app.core.config import settings


if cloudinary is not None and settings is not None:
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True,
    )


async def upload_image_to_cloudinary(file_bytes: Any, public_id: Optional[str] = None) -> dict:
    if cloudinary is None or cloudinary.uploader is None:
        raise RuntimeError("cloudinary package is not installed")
    if not settings.CLOUDINARY_CLOUD_NAME or not settings.CLOUDINARY_API_KEY or not settings.CLOUDINARY_API_SECRET:
        raise RuntimeError("Cloudinary credentials are not configured")

    payload = file_bytes
    if isinstance(file_bytes, str):
        payload = BytesIO(file_bytes.encode("utf-8"))

    return cloudinary.uploader.upload(
        payload,
        public_id=public_id or f"uploads/{uuid4().hex}",
        overwrite=True,
        resource_type="image",
    )
