from typing import Optional
from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    sku: str
    barcode: str
    price: float = Field(gt=0)
    cost: Optional[float] = Field(gt=0, default=None)
    quantity: int = Field(ge=0)
    min_quantity: int = Field(ge=0, default=0)
    is_active: bool = True

class ProductCreate(ProductBase):
    manufacturer_id: int

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    sku: Optional[str] = None
    barcode: Optional[str] = None
    price: Optional[float] = Field(gt=0, default=None)
    manufacturer_id: Optional[int] = None

class ProductInDBBase(ProductBase):
    id: int
    manufacturer_id: int

    class Config:
        from_attributes = True

class Product(ProductInDBBase):
    pass

class ProductInDB(ProductInDBBase):
    pass 