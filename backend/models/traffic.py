from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from enum import Enum

class SignalState(str, Enum):
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"

class LaneDensity(BaseModel):
    lane_id: str
    vehicle_count: int = Field(default=0, ge=0)
    has_emergency_vehicle: bool = False
    average_speed_kmh: Optional[float] = 40.0

class JunctionState(BaseModel):
    junction_id: str
    active_lane: str
    signal_states: Dict[str, SignalState]
    current_green_duration: int
    remaining_green_time: int
    densities: Dict[str, int]
    emergency_override: bool = False