
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from datetime import date
import logging
import asyncio

logger = logging.getLogger(__name__)
router = APIRouter(tags=["pdf"])

@router.get("/report/pdf")
async def get_report_pdf(
    requestId: str = Query(..., description="Request id")
):
    file_path = f"storage/{requestId}/report.pdf"

    if not Path(file_path).exists():
        raise HTTPException(status_code=422, detail=f"File not found: {file_path}")

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"inline; filename=\"report_{date.today()}.pdf\"",
            "Cache-Control": "no-cache",
            "X-Content-Type-Options": "nosniff"
        }
    ) 
