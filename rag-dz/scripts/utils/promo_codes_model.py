# backend/rag-compat/app/models/promo_codes.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ARRAY
from datetime import datetime, timedelta
from ..database import Base

class PromoCode(Base):
    __tablename__ = "promo_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)  # "LAUNCH30"
    discount_percent = Column(Integer)  # 25 ou 33
    max_uses = Column(Integer)  # 30
    current_uses = Column(Integer, default=0)
    valid_from = Column(DateTime, default=datetime.utcnow)
    valid_until = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Restrictions
    applicable_packages = Column(ARRAY(String))  # ["starter", "dev"]
    duration_months = Column(Integer)  # 6

# SQL pour créer le promo code "LAUNCH30"
"""
INSERT INTO promo_codes (
    code,
    discount_percent,
    max_uses,
    valid_until,
    applicable_packages,
    duration_months
) VALUES
('LAUNCH30', 25, 30, '2026-01-07', ARRAY['starter', 'dev'], 6);
"""
