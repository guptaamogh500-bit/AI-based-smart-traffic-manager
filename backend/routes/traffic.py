from fastapi import APIRouter
from typing import List
from models.traffic import LaneDensity, JunctionState
from services.signal_service import signal_service

router = APIRouter()

@router.post("/update-density", response_model=JunctionState)
async def update_density(densities: List[LaneDensity]):
    active_lane, duration, override = signal_service.evaluate_next_phase(densities)
    return JunctionState(
        junction_id=signal_service.junction_id,
        active_lane=active_lane,
        signal_states=signal_service.get_signal_states(active_lane),
        current_green_duration=duration,
        remaining_green_time=signal_service.remaining_green_time,
        densities=signal_service.current_densities,
        emergency_override=override
    )