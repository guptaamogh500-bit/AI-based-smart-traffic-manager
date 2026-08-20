import cv2
import time
import requests
import os
from detection.detector import VehicleDetector

API_UPDATE_URL = "http://localhost:8000/api/traffic/update-density"

# Update the paths to point outside the 'ai' folder to the root 'data' folder
LANES = {
    "Lane_North": "../data/videos/north.mp4",
    "Lane_South": "../data/videos/south.mp4",
    "Lane_East": "../data/videos/east.mp4",
    "Lane_West": "../data/videos/west.mp4"
}

def main():
    detector = VehicleDetector()
    video_captures = {}

    for lane_id, src in LANES.items():
        if os.path.exists(src) or isinstance(src, int):
            video_captures[lane_id] = cv2.VideoCapture(src)

    print("AI Traffic Loop Running. Press Ctrl+C to stop.")

    while True:
        lane_payload = []

        for lane_id, cap in video_captures.items():
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            count, emergency = detector.detect_frame(frame)
            lane_payload.append({
                "lane_id": lane_id,
                "vehicle_count": count,
                "has_emergency_vehicle": emergency
            })

        # Fallback dummy simulation if video files are missing
        if not video_captures:
            lane_payload = [
                {"lane_id": "Lane_North", "vehicle_count": 12, "has_emergency_vehicle": False},
                {"lane_id": "Lane_South", "vehicle_count": 4, "has_emergency_vehicle": False},
                {"lane_id": "Lane_East", "vehicle_count": 22, "has_emergency_vehicle": False},
                {"lane_id": "Lane_West", "vehicle_count": 8, "has_emergency_vehicle": False},
            ]

        if lane_payload:
            try:
                res = requests.post(API_UPDATE_URL, json=lane_payload, timeout=2.0)
                print(f"[AI Sync] Density sent -> HTTP {res.status_code}")
            except Exception as err:
                print(f"[Sync Error] Backend offline: {err}")

        time.sleep(2.0)

if __name__ == "__main__":
    main()