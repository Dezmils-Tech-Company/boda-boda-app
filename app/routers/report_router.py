from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_user, require_admin
from app.services.report_service import generate_and_upload_report

router = APIRouter()


@router.post("/reports/generate")
async def generate_report(title: str, content: str, current_user=Depends(require_admin)):
    try:
        content_lines = [line.strip() for line in content.splitlines() if line.strip()]
        result = await generate_and_upload_report(title=title, content_lines=content_lines)
        return {
            "status": "success",
            "message": "Report generated and stored in Cloudinary",
            "data": {
                "title": title,
                "url": result.get("secure_url"),
                "public_id": result.get("public_id"),
            },
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(exc)}") from exc
