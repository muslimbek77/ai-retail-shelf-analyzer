from functools import lru_cache
from pathlib import Path

from huggingface_hub import hf_hub_download
from ultralytics import YOLO

from app.config import MODEL_PATH


@lru_cache(maxsize=1)
def get_model() -> YOLO:
    # COCO weights do not have a class for packaged grocery products. Use a
    # shelf-specific SKU-110K checkpoint by default; allow local weights via env.
    model_path = MODEL_PATH or hf_hub_download(
        repo_id="jz67/localfirst-vision-yolo",
        filename="sku110k-yolov8n.pt",
    )
    return YOLO(model_path)


def detect(image_path: Path) -> tuple[list[dict], object]:
    """Return normalized detections and an annotated BGR image."""
    model = get_model()
    result = model.predict(
        source=str(image_path), conf=0.25, iou=0.55, imgsz=960, verbose=False
    )[0]
    names = result.names
    detections = []
    for box in result.boxes:
        class_id = int(box.cls.item())
        coords = [round(float(value), 2) for value in box.xyxy[0].tolist()]
        detections.append({
            "class_id": class_id,
            "label": "mahsulot" if class_id == 0 else str(names[class_id]),
            "confidence": round(float(box.conf.item()), 4),
            "box": coords,
        })
    return detections, result.plot()
