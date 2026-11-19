from functools import lru_cache
from pathlib import Path

from ultralytics import YOLO

from app.config import MODEL_PATH


@lru_cache(maxsize=1)
def get_model() -> YOLO:
    return YOLO(MODEL_PATH)


def detect(image_path: Path) -> tuple[list[dict], object]:
    """Return normalized detections and an annotated BGR image."""
    model = get_model()
    result = model.predict(source=str(image_path), verbose=False)[0]
    names = result.names
    detections = []
    for box in result.boxes:
        class_id = int(box.cls.item())
        coords = [round(float(value), 2) for value in box.xyxy[0].tolist()]
        detections.append({
            "class_id": class_id,
            "label": str(names[class_id]),
            "confidence": round(float(box.conf.item()), 4),
            "box": coords,
        })
    return detections, result.plot()
