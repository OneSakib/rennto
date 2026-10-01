from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class UserOut(ORMModel):
    id: int
    name: str
    email: str

class TenantCreate(BaseModel):
    name: str
    phone: str
    property_name: str
    start_date: date
    notes: str | None = None

class TenantOut(ORMModel):
    id: int
    name: str
    phone: str
    property_name: str
    start_date: date
    status: bool
    notes: str | None

class PlanCreate(BaseModel):
    name: str
    amount: Decimal
    frequency: str = "monthly"
    due_day: int = 1
    start_date: date

class PlanOut(ORMModel):
    id: int
    name: str
    amount: Decimal
    frequency: str
    due_day: int
    start_date: date
    status: bool

class AssignPlan(BaseModel):
    plan_id: int
    start_date: date

class PaymentCreate(BaseModel):
    amount: Decimal
    payment_date: date
    payment_method: str = "cash"
    notes: str | None = None

class DiscountCreate(BaseModel):
    amount: Decimal
    reason: str | None = None

class RentOut(ORMModel):
    id: int
    tenant_id: int
    plan_id: int
    billing_month: str
    due_date: date
    amount: Decimal
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut
