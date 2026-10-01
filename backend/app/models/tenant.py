from datetime import datetime, date
from sqlalchemy import String, DateTime, Date, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Tenant(Base):
    __tablename__ = "tenants"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    phone: Mapped[str] = mapped_column(String(30))
    property_name: Mapped[str] = mapped_column(String(150))
    start_date: Mapped[date] = mapped_column(Date)
    status: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    owner = relationship("User", back_populates="tenants")
    tenant_plans = relationship("TenantPlan", back_populates="tenant", cascade="all, delete-orphan")
    rents = relationship("Rent", back_populates="tenant", cascade="all, delete-orphan")
