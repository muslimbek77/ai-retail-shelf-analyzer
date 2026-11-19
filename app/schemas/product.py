from datetime import datetime

from pydantic import BaseModel


class ProductRead(BaseModel):
    id: int
    name: str
    category: str
    brand: str | None = None
    package_size: str | None = None
    reference_image_url: str
    created_at: datetime | None = None
