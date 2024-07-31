from fastapi import APIRouter, Query, Depends, HTTPException, Request
from app.services.data_service import DataService
from pydantic import BaseModel, field_validator, ValidationInfo

from typing import Optional, List
from datetime import datetime

router = APIRouter()

def get_data_service(request: Request):
    return request.app.state.data_service

class StatsParams(BaseModel):
    channels: Optional[List[str]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    @field_validator('start_date', 'end_date', mode='before')
    @classmethod
    def parse_datetime(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError("Invalid datetime format. Use YYYY-MM-DD HH:MM:SS.")
        return value

    @field_validator('end_date')
    @classmethod
    def end_date_after_start_date(cls, v: Optional[datetime], info: ValidationInfo) -> Optional[datetime]:
        if v and info.data.get('start_date') and v <= info.data['start_date']:
            raise ValueError("end_date must be after start_date")
        return v


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
        params = StatsParams(
            channels=channels,
            start_date=start_date,
            end_date=end_date
        )

        # Validate channels if provided
        if params.channels:
            # Check if there are ANY entities that are not in the data_service.get_channels()
            invalid_channels = set(params.channels) - set(data_service.get_channels())
            if invalid_channels:
                raise HTTPException(status_code=400, detail=f"Invalid channel(s): {', '.join(invalid_channels)}")

        stats = data_service.get_stats(
            channels=params.channels,
            start_date=params.start_date.strftime("%Y-%m-%d %H:%M:%S") if params.start_date else None,
            end_date=params.end_date.strftime("%Y-%m-%d %H:%M:%S") if params.end_date else None
        )

        if not stats:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")

        return stats

    except HTTPException as he:
        # Re-raise HTTP exceptions without catching them
        raise he
    except ValueError as ve:
        # Bad request for validation errors
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Unexpected errors
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {str(e)}")
