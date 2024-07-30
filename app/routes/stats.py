from fastapi import APIRouter, Query, Depends, HTTPException, Request
from app.services.data_service import DataService

from typing import Optional, List
from datetime import datetime

router = APIRouter()

def get_data_service(request: Request):
    return request.app.state.data_service

@router.get("/stats")
async def get_stats(
    channels: Optional[List[str]] = Query(None, description="List of channel names to calculate stats for"),
    start_date: Optional[str] = Query(None, description="Start datetime for the stats calculation (format: YYYY-MM-DD HH:MM:SS)"),
    end_date: Optional[str] = Query(None, description="End datetime for the stats calculation (format: YYYY-MM-DD HH:MM:SS)"),
    data_service: DataService = Depends(get_data_service)
):
    """
    Calculate statistics for the specified channels within the given datetime range.
    - **channels**: Optional list of channel names to calculate stats for. If not provided, stats for all channels are returned.
    - **start_date**: Optional start datetime for the stats calculation (format: YYYY-MM-DD HH:MM:SS). If not provided, the earliest datetime in the dataset is used.
    - **end_date**: Optional end datetime for the stats calculation (format: YYYY-MM-DD HH:MM:SS). If not provided, the latest datetime in the dataset is used.
    """
    try:
        # Validate channels if provided
        if channels:
            invalid_channels = [ch for ch in channels if ch not in data_service.get_channels()]
            if invalid_channels:
                raise HTTPException(status_code=400, detail=f"Invalid channel(s): {', '.join(invalid_channels)}")

        # Validate and parse datetimes
        try:
            if start_date:
                start_date = datetime.fromisoformat(start_date).strftime("%Y-%m-%d %H:%M:%S")
            if end_date:
                end_date = datetime.fromisoformat(end_date).strftime("%Y-%m-%d %H:%M:%S")
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=f"Invalid datetime format: {str(ve)}. Use YYYY-MM-DD HH:MM:SS.")

        stats = data_service.get_stats(channels, start_date, end_date)

        if not stats:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")

        return stats
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {str(e)}")
