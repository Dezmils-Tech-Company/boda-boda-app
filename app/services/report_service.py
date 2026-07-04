from io import BytesIO
from typing import List, Optional
from uuid import uuid4

from loguru import logger

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


def build_simple_pdf(title: str, content_lines: List[str]) -> bytes:
    buffer = BytesIO()
    buffer.write(b"%PDF-1.4\n")

    text = "\n".join(content_lines)
    payload = (
        f"BT\n/F1 12 Tf\n72 770 Td\n({title}) Tj\n0 -20 Td\n({text}) Tj\nET\n"
    ).encode("latin-1", "replace")

    buffer.write(payload)
    buffer.write(b"endobj")
    return buffer.getvalue()


async def upload_report_pdf(pdf_bytes: bytes, public_id: Optional[str] = None) -> dict:
    if cloudinary is None or cloudinary.uploader is None:
        raise RuntimeError("cloudinary package is not installed")
    if not settings.CLOUDINARY_CLOUD_NAME or not settings.CLOUDINARY_API_KEY or not settings.CLOUDINARY_API_SECRET:
        raise RuntimeError("Cloudinary credentials are not configured")

    upload_result = cloudinary.uploader.upload(
        BytesIO(pdf_bytes),
        resource_type="raw",
        public_id=public_id or f"reports/{uuid4().hex}",
        format="pdf",
        overwrite=True,
    )
    return upload_result


async def generate_and_upload_report(title: str, content_lines: List[str], public_id: Optional[str] = None) -> dict:
    pdf_bytes = build_simple_pdf(title=title, content_lines=content_lines)
    result = await upload_report_pdf(pdf_bytes, public_id=public_id)
    logger.info("Uploaded report to Cloudinary", public_id=result.get("public_id"))
    return result
