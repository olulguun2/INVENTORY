from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_product
from app.models.user import User
from app.schemas.product import Product, ProductCreate, ProductUpdate

router = APIRouter()

@router.get("/", response_model=List[Product])
def read_products(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve products.
    """
    if current_user.role == "manufacturer":
        products = crud_product.get_by_manufacturer(
            db, manufacturer_id=current_user.id, skip=skip, limit=limit
        )
    else:
        products = crud_product.get_multi(db, skip=skip, limit=limit)
    return products

@router.post("/", response_model=Product)
def create_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: ProductCreate,
    current_user: User = Depends(deps.get_current_manufacturer_user),
) -> Any:
    """
    Create new product.
    """
    product = crud_product.get_by_sku(db, sku=product_in.sku)
    if product:
        raise HTTPException(
            status_code=400,
            detail="Product with this SKU already exists.",
        )
    product = crud_product.get_by_barcode(db, barcode=product_in.barcode)
    if product:
        raise HTTPException(
            status_code=400,
            detail="Product with this barcode already exists.",
        )
    product = crud_product.create(db, obj_in=product_in)
    return product

@router.put("/{product_id}", response_model=Product)
def update_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    product_in: ProductUpdate,
    current_user: User = Depends(deps.get_current_manufacturer_user),
) -> Any:
    """
    Update a product.
    """
    product = crud_product.get(db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.manufacturer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    product = crud_product.update(db, db_obj=product, obj_in=product_in)
    return product

@router.get("/{product_id}", response_model=Product)
def read_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get product by ID.
    """
    product = crud_product.get(db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}", response_model=Product)
def delete_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    current_user: User = Depends(deps.get_current_manufacturer_user),
) -> Any:
    """
    Delete a product.
    """
    product = crud_product.get(db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.manufacturer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    product = crud_product.remove(db, id=product_id)
    return product

@router.get("/low-stock/", response_model=List[Product])
def read_low_stock_products(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_manufacturer_user),
) -> Any:
    """
    Retrieve products with low stock.
    """
    products = crud_product.get_low_stock(
        db, manufacturer_id=current_user.id, skip=skip, limit=limit
    )
    return products

@router.post("/{product_id}/update-stock")
def update_product_stock(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    quantity_change: int,
    current_user: User = Depends(deps.get_current_manufacturer_user),
) -> Any:
    """
    Update product stock quantity.
    """
    product = crud_product.get(db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.manufacturer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    product = crud_product.update_stock(
        db, product_id=product_id, quantity_change=quantity_change
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Stock updated successfully"} 