from fastapi import APIRouter
from pydantic import BaseModel
from services.signal_service import signal_service

router = APIRouter()

class EmergencyOverrideRequest(BaseModel):
    lane_id: str
    duration_seconds: int = 45

@router.post("/override")
async def trigger_override(req: EmergencyOverrideRequest):
    signal_service.emergency_override = True
    signal_service.remaining_green_time = req.duration_seconds
    signal_service.current_green_duration = req.duration_seconds
    return {"status": "emergency_activated", "lane": req.lane_id, "duration": req.duration_seconds}