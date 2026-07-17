from sqlalchemy import Column, String, ForeignKey, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid

class Scan(Base):
    __tablename__ = "scans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    batch_id = Column(UUID(as_uuid=True), ForeignKey("batches.id"))

    location = Column(String)
    image_score = Column(Float)
    qr_valid = Column(Boolean)
    batch_match = Column(Boolean)
    expiry_valid = Column(Boolean)
    risk_score = Column(Float)
    verdict = Column(String)
    reason = Column(String)