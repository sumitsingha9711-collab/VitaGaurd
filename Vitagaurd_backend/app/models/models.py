from sqlalchemy import Column, Index, String, Date, Boolean, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP
from app.db.base import Base
import uuid

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    brand = Column(String)
    category = Column(String)
    gtin = Column(String)
    manufacturer = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Batch(Base):
    __tablename__ = "batches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    batch_number = Column(String)
    manufacturing_date = Column(Date)
    expiry_date = Column(Date)
    is_active = Column(Boolean)

class Scan(Base):
    __tablename__ = "scans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    batch_id = Column(UUID(as_uuid=True), ForeignKey("batches.id"), nullable=True)

    location = Column(String, nullable=False)

    image_score = Column(Float, nullable=False)
    qr_valid = Column(Boolean, default=True)
    batch_match = Column(Boolean, default=True)
    expiry_valid = Column(Boolean, default=True)

    risk_score = Column(Float, nullable=False)
    verdict = Column(String, nullable=False)

    reason = Column(String)  # explanation for flag

    scanned_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (
        Index("idx_product_scan", "product_id"),
    )