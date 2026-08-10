from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.product import Product
from app.models.batch import Batch
from app.models.scan import Scan
from app.services.risk_engine import RiskEngine
from app.schemas.scan import ScanRequest, ScanResponse
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/scan", tags=["Scan"])


@router.post("/", response_model=ScanResponse)
def scan_product(
    request: ScanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 🔹 Check product existence
    product = db.query(Product).filter(
        Product.id == request.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # 🔹 Check batch
    batch = db.query(Batch).filter(
        Batch.product_id == request.product_id,
        Batch.batch_number == request.batch_number
    ).first()

    batch_match = batch is not None
    expiry_valid = True

    if batch and batch.expiry_date:
        if batch.expiry_date < date.today():
            expiry_valid = False

    # 🔹 Simulated AI packaging score (future ML integration point)
    image_score = 0.85
    qr_valid = True

    # 🔹 Risk Evaluation
    risk_score, verdict, breakdown = RiskEngine.calculate(
        image_score=image_score,
        batch_match=batch_match,
        expiry_valid=expiry_valid
    )

    # 🔹 Store scan
    new_scan = Scan(
        product_id=product.id,
        batch_id=batch.id if batch else None,
        location=request.location,
        device_id=request.device_id,
        user_id=request.user_id,
        latitude=request.latitude,
        longitude=request.longitude,
        scan_timestamp=request.scan_timestamp,
        image_score=image_score,
        qr_valid=qr_valid,
        batch_match=batch_match,
        expiry_valid=expiry_valid,
        risk_score=risk_score,
        verdict=verdict,
        reason="Automated AI risk evaluation"
    )

    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)

    return ScanResponse(
        scan_id=new_scan.id,
        risk_score=risk_score,
        verdict=verdict,
        breakdown=breakdown
    )