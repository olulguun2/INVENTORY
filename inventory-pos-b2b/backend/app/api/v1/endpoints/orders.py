from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_order, crud_product
from app.models.user import User
from app.models.order import OrderStatus
from app.schemas.order import Order, OrderCreate, OrderUpdate

router = APIRouter()

@router.get("/", response_model=List[Order])
def read_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve orders.
    """
    if current_user.role == "store":
        orders = crud_order.get_by_store(
            db, store_id=current_user.id, skip=skip, limit=limit
        )
    elif current_user.role == "manufacturer":
        # For manufacturers, get orders containing their products
        orders = crud_order.get_by_status(
            db, status=OrderStatus.PENDING, skip=skip, limit=limit
        )
    else:
        orders = crud_order.get_multi(db, skip=skip, limit=limit)
    return orders

@router.post("/", response_model=Order)
def create_order(
    *,
    db: Session = Depends(deps.get_db),
    order_in: OrderCreate,
    current_user: User = Depends(deps.get_current_store_user),
) -> Any:
    """
    Create new order.
    """
    # Verify all products exist and have sufficient stock
    for item in order_in.items:
        product = crud_product.get(db, id=item.product_id)
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product with ID {item.product_id} not found.",
            )
        if product.quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product {product.name}.",
            )
    
    # Create order with items
    order = crud_order.create_with_items(
        db, obj_in=order_in, items=[item.dict() for item in order_in.items]
    )
    return order

@router.get("/{order_id}", response_model=Order)
def read_order(
    *,
    db: Session = Depends(deps.get_db),
    order_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get order by ID.
    """
    order = crud_order.get(db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if current_user.role == "store" and order.store_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return order

@router.put("/{order_id}/status")
def update_order_status(
    *,
    db: Session = Depends(deps.get_db),
    order_id: int,
    status: OrderStatus,
    current_user: User = Depends(deps.get_current_manufacturer_user),
) -> Any:
    """
    Update order status.
    """
    order = crud_order.get(db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Update order status
    order = crud_order.update_status(db, order_id=order_id, status=status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # If order is confirmed, update product quantities
    if status == OrderStatus.CONFIRMED:
        for item in order.items:
            product = crud_product.get(db, id=item.product_id)
            if product:
                crud_product.update_stock(
                    db, product_id=product.id, quantity_change=-item.quantity
                )
    
    return {"message": "Order status updated successfully"} 