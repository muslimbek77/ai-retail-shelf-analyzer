import json
import uuid
from pathlib import Path

import cv2
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.config import ALLOWED_CONTENT_TYPES, MAX_UPLOAD_BYTES, RESULT_DIR, UPLOAD_DIR
from app.database import get_db
from app.models import Analysis
from app.schemas.analysis import AnalysisHistoryItem, AnalysisResult
from app.services.detector import detect

router = APIRouter(prefix="/api/analyses", tags=["analyses"])


@router.post("", response_model=AnalysisResult)
async def create_analysis(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=415, detail="JPEG, PNG yoki WebP rasm yuklang")
    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if not content:
        raise HTTPException(status_code=400, detail="Rasm bo'sh")
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Rasm hajmi 15 MB dan oshmasligi kerak")

    suffix = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}[file.content_type]
    key = uuid.uuid4().hex
    input_path = UPLOAD_DIR / f"{key}{suffix}"
    output_path = RESULT_DIR / f"{key}.jpg"
    input_path.write_bytes(content)
    image = cv2.imread(str(input_path))
    if image is None:
        input_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail="Yuklangan fayl yaroqli rasm emas")
    try:
        detections, annotated = detect(input_path)
        if not cv2.imwrite(str(output_path), annotated):
            raise RuntimeError("Natija rasmini saqlab bo'lmadi")
    except Exception as exc:
        input_path.unlink(missing_ok=True)
        output_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=f"Rasm tahlilida xatolik: {exc}") from exc

    row = Analysis(
        original_filename=Path(file.filename or "image").name,
        image_path=str(input_path),
        result_path=str(output_path),
        detections_json=json.dumps(detections, ensure_ascii=False),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return AnalysisResult(
        id=row.id, filename=row.original_filename, detections=detections,
        result_image_url=f"/results/{output_path.name}", created_at=row.created_at,
    )


@router.get("", response_model=list[AnalysisHistoryItem])
def list_analyses(limit: int = 20, db: Session = Depends(get_db)):
    if not 1 <= limit <= 100:
        raise HTTPException(status_code=422, detail="limit 1 dan 100 gacha bo'lishi kerak")
    rows = db.query(Analysis).order_by(Analysis.id.desc()).limit(limit).all()
    return [AnalysisHistoryItem(
        id=row.id,
        filename=row.original_filename,
        detections_count=len(json.loads(row.detections_json)),
        result_image_url=f"/results/{Path(row.result_path).name}",
        created_at=row.created_at,
    ) for row in rows]
