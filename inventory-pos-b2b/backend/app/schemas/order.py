from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.order import OrderStatus

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    subtotal: float = Field(gt=0)

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(OrderItemBase):
    product_id: Optional[int] = None
    quantity: Optional[int] = Field(gt=0, default=None)
    unit_price: Optional[float] = Field(gt=0, default=None)
    subtotal: Optional[float] = Field(gt=0, default=None)

class OrderItemInDBBase(OrderItemBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True

class OrderItem(OrderItemInDBBase):
    pass

class OrderBase(BaseModel):
    shipping_address: str
    notes: Optional[str] = None

class OrderCreate(OrderBase):
    store_id: int
    items: List[OrderItemCreate]

class OrderUpdate(OrderBase):
    status: Optional[OrderStatus] = None
    shipping_address: Optional[str] = None
    items: Optional[List[OrderItemCreate]] = None

class OrderInDBBase(OrderBase):
    id: int
    order_number: str
    store_id: int
    status: OrderStatus
    total_amount: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Order(OrderInDBBase):
    items: List[OrderItem]

class OrderInDB(OrderInDBBase):
    pass 