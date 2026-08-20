from typing import Dict, Tuple, List
from models.traffic import LaneDensity, SignalState

MIN_GREEN = 10
MAX_GREEN = 60

class SignalService:
    def __init__(self, junction_id: str = "JUNCTION_01", lanes: List[str] = None):
        self.junction_id = junction_id
        self.lanes = lanes or ["Lane_North", "Lane_South", "Lane_East", "Lane_West"]
        self.active_lane_index = 0
        self.current_green_duration = MIN_GREEN
        self.remaining_green_time = MIN_GREEN
        self.emergency_override = False
        self.current_densities: Dict[str, int] = {lane: 0 for lane in self.lanes}

    def compute_green_time(self, lane_count: int, total_count: int) -> int:
        if total_count == 0:
            return MIN_GREEN
        ratio = lane_count / total_count
        duration = int(MIN_GREEN + ratio * (MAX_GREEN - MIN_GREEN))
        return max(MIN_GREEN, min(MAX_GREEN, duration))

    def evaluate_next_phase(self, lane_data: List[LaneDensity]) -> Tuple[str, int, bool]:
        for lane in lane_data:
            self.current_densities[lane.lane_id] = lane.vehicle_count
            if lane.has_emergency_vehicle:
                self.emergency_override = True
                self.remaining_green_time = MAX_GREEN
                self.current_green_duration = MAX_GREEN
                return lane.lane_id, MAX_GREEN, True

        self.emergency_override = False
        total_vehicles = sum(l.vehicle_count for l in lane_data)
        
        self.active_lane_index = (self.active_lane_index + 1) % len(self.lanes)
        next_lane = self.lanes[self.active_lane_index]
        green_duration = self.compute_green_time(self.current_densities.get(next_lane, 0), total_vehicles)
        
        self.current_green_duration = green_duration
        self.remaining_green_time = green_duration
        return next_lane, green_duration, False

    def get_signal_states(self, active_lane: str) -> Dict[str, SignalState]:
        return {
            lane: SignalState.GREEN if lane == active_lane else SignalState.RED
            for lane in self.lanes
        }

signal_service = SignalService()