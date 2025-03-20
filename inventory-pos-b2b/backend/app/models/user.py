from sqlalchemy import Boolean, Column, Integer, String, Enum
from app.models.base import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    STORE = "store"
    MANUFACTURER = "manufacturer"

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    company_name = Column(String)  # For store or manufacturer
    phone = Column(String)
    address = Column(String) 