import torch

MODEL_PATH = r"C:\Users\agamw\.cache\huggingface\hub\models--iisc-aim--UVH-26\snapshots\4a22412775adb6f97f22735647afee976b4638a0\weights\YOLOv11-S\UVH-26-MV-YOLOv11-S.pt"

CONFIDENCE_THRESHOLD = 0.35
IMAGE_SIZE = 1280
DEVICE = 0 if torch.cuda.is_available() else "cpu"