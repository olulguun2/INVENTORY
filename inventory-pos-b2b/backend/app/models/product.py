from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import Base

class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    sku = Column(String, unique=True, index=True)
    barcode = Column(String, unique=True, index=True)
    price = Column(Float, nullable=False)
    cost = Column(Float)  # Cost price for manufacturers
    quantity = Column(Integer, default=0)
    min_quantity = Column(Integer, default=0)  # Minimum stock level
    manufacturer_id = Column(Integer, ForeignKey("user.id"))
    is_active = Column(Boolean, default=True)
    
    # Relationships
    manufacturer = relationship("User", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product") 