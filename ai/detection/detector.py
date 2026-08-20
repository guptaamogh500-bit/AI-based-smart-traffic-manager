import numpy as np
from ultralytics import YOLO
from detection.config import MODEL_PATH, CONFIDENCE_THRESHOLD, IMAGE_SIZE, DEVICE
from detection.classes import EMERGENCY_CLASSES, UVH_26_CLASSES

class VehicleDetector:
    def __init__(self):
        print(f"Loading UVH-26 Model from: {MODEL_PATH}")
        self.model = YOLO(MODEL_PATH)
        self.device = DEVICE
        self.conf = CONFIDENCE_THRESHOLD
        self.imgsz = IMAGE_SIZE
        print(f"Detector ready on {self.device}")

    def detect_frame(self, frame: np.ndarray) -> tuple[int, bool]:
        results = self.model.predict(
            source=frame,
            conf=self.conf,
            imgsz=self.imgsz,
            device=self.device,
            verbose=False
        )

        result = results[0]
        vehicle_count = 0
        has_emergency = False

        if result.boxes is not None:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = UVH_26_CLASSES.get(class_id, "Other").lower()
                vehicle_count += 1

                if any(emg in class_name for emg in EMERGENCY_CLASSES):
                    has_emergency = True

        return vehicle_count, has_emergency