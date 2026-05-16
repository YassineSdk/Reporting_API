from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["tables"])

@router.get("/tables")
async def get_tables(
    requestId: str = Query(..., description="Request id")
):
    file_path = f"storage/{requestId}/tables.xls"

    if not Path(file_path).exists():
        raise HTTPException(status_code=422, detail=f"File not found: {file_path}")

    return FileResponse(
        path=file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=f"table{requestId}.xls"
    )