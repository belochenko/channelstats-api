from fastapi import APIRouter, Query, Depends
from typing import Optional
from app.services.data_service import DataService
from fastapi import Request

router = APIRouter()

def get_data_service(request: Request):
    return request.app.state.data_service

@router.get("/channels")
async def get_channels(
    channel_type: Optional[str] = Query(None, description="Filter channels by type (e.g., 'vel', 'std', 'temp')"),
    data_service: DataService = Depends(get_data_service)
):
    """
    Get the available channels from the dataset.

    - **channel_type**: Optional filter to return only channels of the specified type.
    """
    channels = data_service.get_channels(channel_type)
    return {"channels": channels}
