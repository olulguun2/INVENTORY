from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_by_sku(self, db: Session, *, sku: str) -> Optional[Product]:
        return db.query(Product).filter(Product.sku == sku).first()
    
    def get_by_barcode(self, db: Session, *, barcode: str) -> Optional[Product]:
        return db.query(Product).filter(Product.barcode == barcode).first()
    
    def get_by_manufacturer(
        self, db: Session, *, manufacturer_id: int, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        return (
            db.query(Product)
            .filter(Product.manufacturer_id == manufacturer_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_low_stock(
        self, db: Session, *, manufacturer_id: int, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        return (
            db.query(Product)
            .filter(
                Product.manufacturer_id == manufacturer_id,
                Product.quantity <= Product.min_quantity
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def update_stock(
        self, db: Session, *, product_id: int, quantity_change: int
    ) -> Optional[Product]:
        product = self.get(db, id=product_id)
        if not product:
            return None
        product.quantity += quantity_change
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

product = CRUDProduct(Product) 