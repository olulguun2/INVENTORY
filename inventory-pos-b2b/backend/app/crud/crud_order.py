from typing import List, Optional
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order import OrderCreate, OrderUpdate

class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def get_by_order_number(self, db: Session, *, order_number: str) -> Optional[Order]:
        return db.query(Order).filter(Order.order_number == order_number).first()
    
    def get_by_store(
        self, db: Session, *, store_id: int, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        return (
            db.query(Order)
            .filter(Order.store_id == store_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_status(
        self, db: Session, *, status: OrderStatus, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        return (
            db.query(Order)
            .filter(Order.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create_with_items(
        self, db: Session, *, obj_in: OrderCreate, items: List[dict]
    ) -> Order:
        # Generate unique order number
        order_number = f"ORD-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8]}"
        
        # Calculate total amount
        total_amount = sum(item["subtotal"] for item in items)
        
        # Create order
        db_obj = Order(
            order_number=order_number,
            store_id=obj_in.store_id,
            status=OrderStatus.PENDING,
            total_amount=total_amount,
            shipping_address=obj_in.shipping_address,
            notes=obj_in.notes
        )
        db.add(db_obj)
        db.flush()  # Get the order ID
        
        # Create order items
        for item in items:
            order_item = OrderItem(
                order_id=db_obj.id,
                product_id=item["product_id"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                subtotal=item["subtotal"]
            )
            db.add(order_item)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update_status(
        self, db: Session, *, order_id: int, status: OrderStatus
    ) -> Optional[Order]:
        order = self.get(db, id=order_id)
        if not order:
            return None
        order.status = status
        db.add(order)
        db.commit()
        db.refresh(order)
        return order

order = CRUDOrder(Order) 