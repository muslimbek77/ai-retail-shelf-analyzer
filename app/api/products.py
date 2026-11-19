import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.config import ALLOWED_CONTENT_TYPES, CATALOG_DIR, MAX_UPLOAD_BYTES
from app.database import get_db
from app.models import Product
from app.schemas.product import ProductRead

router = APIRouter(prefix="/api/products", tags=["products"])


def as_product_read(product: Product) -> ProductRead:
    return ProductRead(
        id=product.id,
        name=product.name,
        category=product.category,
        brand=product.brand,
        package_size=product.package_size,
        reference_image_url=f"/catalog-images/{Path(product.reference_image).name}",
        created_at=product.created_at,
    )


@router.get("", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)):
    return [as_product_read(item) for item in db.query(Product).order_by(Product.name).all()]


@router.post("", response_model=ProductRead, status_code=201)
async def create_product(
    name: str = Form(..., min_length=1, max_length=255),
    category: str = Form(..., min_length=1, max_length=120),
    brand: str | None = Form(None, max_length=120),
    package_size: str | None = Form(None, max_length=120),
    reference_image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if reference_image.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=415, detail="Etalon rasm JPEG, PNG yoki WebP bo'lishi kerak")
    content = await reference_image.read(MAX_UPLOAD_BYTES + 1)
    if not content or len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Etalon rasm bo'sh yoki 15 MB dan katta")

    suffix = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}[reference_image.content_type]
    image_path = CATALOG_DIR / f"{uuid.uuid4().hex}{suffix}"
    image_path.write_bytes(content)
    product = Product(
        name=name.strip(),
        category=category.strip(),
        brand=brand.strip() if brand and brand.strip() else None,
        package_size=package_size.strip() if package_size and package_size.strip() else None,
        reference_image=str(image_path),
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return as_product_read(product)


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Mahsulot topilmadi")
    Path(product.reference_image).unlink(missing_ok=True)
    db.delete(product)
    db.commit()
