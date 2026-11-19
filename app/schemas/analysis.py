from datetime import datetime
from pydantic import BaseModel, ConfigDict


class Detection(BaseModel):
    class_id: int
    label: str
    confidence: float
    box: list[float]


class AnalysisResult(BaseModel):
    id: int
    filename: str
    detections: list[Detection]
    result_image_url: str
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class AnalysisHistoryItem(BaseModel):
    id: int
    filename: str
    detections_count: int
    result_image_url: str
    created_at: datetime | None = None
