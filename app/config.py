import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", BASE_DIR / "uploads"))
RESULT_DIR = Path(os.getenv("RESULT_DIR", BASE_DIR / "results"))
CATALOG_DIR = Path(os.getenv("CATALOG_DIR", BASE_DIR / "catalog_images"))
DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./shelf_analyzer.db"
)
MODEL_PATH = os.getenv("YOLO_MODEL")
DETECTION_CONFIDENCE = float(os.getenv("YOLO_CONFIDENCE", "0.35"))
DETECTION_IMAGE_SIZE = int(os.getenv("YOLO_IMAGE_SIZE", "960"))
DETECTION_MAX_BOXES = int(os.getenv("YOLO_MAX_DETECTIONS", "1000"))
MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_BYTES", 15 * 1024 * 1024))
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)
CATALOG_DIR.mkdir(parents=True, exist_ok=True)
