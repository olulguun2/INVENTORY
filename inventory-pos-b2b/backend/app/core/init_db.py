from sqlalchemy.orm import Session
from app.crud import crud_user, crud_product
from app.schemas.user import UserCreate
from app.schemas.product import ProductCreate
from app.models.user import UserRole

def init_db(db: Session) -> None:
    # Create admin user
    admin = crud_user.get_by_email(db, email="admin@example.com")
    if not admin:
        admin_in = UserCreate(
            email="admin@example.com",
            password="admin123",
            full_name="Admin User",
            role=UserRole.ADMIN,
            company_name="System Admin",
            phone="1234567890",
            address="System Address"
        )
        crud_user.create(db, obj_in=admin_in)

    # Create sample store user
    store = crud_user.get_by_email(db, email="store@example.com")
    if not store:
        store_in = UserCreate(
            email="store@example.com",
            password="store123",
            full_name="Store User",
            role=UserRole.STORE,
            company_name="Sample Store",
            phone="1234567891",
            address="Store Address"
        )
        crud_user.create(db, obj_in=store_in)

    # Create sample manufacturer user
    manufacturer = crud_user.get_by_email(db, email="manufacturer@example.com")
    if not manufacturer:
        manufacturer_in = UserCreate(
            email="manufacturer@example.com",
            password="manufacturer123",
            full_name="Manufacturer User",
            role=UserRole.MANUFACTURER,
            company_name="Sample Manufacturer",
            phone="1234567892",
            address="Manufacturer Address"
        )
        manufacturer = crud_user.create(db, obj_in=manufacturer_in)

        # Create sample products for the manufacturer
        products = [
            ProductCreate(
                name="Sample Product 1",
                description="A sample product for testing",
                sku="SP001",
                barcode="1234567890123",
                price=99.99,
                cost=50.00,
                quantity=100,
                min_quantity=10,
                manufacturer_id=manufacturer.id
            ),
            ProductCreate(
                name="Sample Product 2",
                description="Another sample product for testing",
                sku="SP002",
                barcode="1234567890124",
                price=149.99,
                cost=75.00,
                quantity=50,
                min_quantity=5,
                manufacturer_id=manufacturer.id
            ),
            ProductCreate(
                name="Sample Product 3",
                description="Yet another sample product for testing",
                sku="SP003",
                barcode="1234567890125",
                price=199.99,
                cost=100.00,
                quantity=25,
                min_quantity=3,
                manufacturer_id=manufacturer.id
            )
        ]

        for product_in in products:
            crud_product.create(db, obj_in=product_in) 