from fastapi import APIRouter
from services.signal_service import signal_service

router = APIRouter()

@router.get("/state")
async def get_current_signals():
    current_active = signal_service.lanes[signal_service.active_lane_index]
    return {
        "junction_id": signal_service.junction_id,
        "active_lane": current_active,
        "signal_states": signal_service.get_signal_states(current_active),
        "remaining_green_time": signal_service.remaining_green_time,
        "emergency_override": signal_service.emergency_override
    }