from datetime import date
from typing import Optional, List

from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse

from app.schemas import Expenses
from app.services.export_service import XLSExport

export_router = APIRouter()


@export_router.get("/export-xls", response_model=List[Expenses])
async def export_xls(
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
):
    export = XLSExport(category, start_date, end_date)
    try:
        export.export()
        return FileResponse("output.xlsx")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error while generating report: {e}")
