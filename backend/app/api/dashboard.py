from decimal import Decimal
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.tenant import Tenant
from app.models.plan import Plan
from app.models.rent import Rent, Payment, Discount

router=APIRouter()

@router.get("")
def dashboard(db:Session=Depends(get_db), user=Depends(get_current_user)):
    tenants=db.query(Tenant).filter(Tenant.user_id==user.id,Tenant.status==True).all()
    plans=db.query(Plan).filter(Plan.user_id==user.id,Plan.status==True).all()
    rents=db.query(Rent).join(Tenant).filter(Tenant.user_id==user.id).all()
    total_rent=sum((Decimal(str(r.amount)) for r in rents),Decimal("0"))
    paid=sum((Decimal(str(p.amount)) for r in rents for p in r.payments),Decimal("0"))
    discount=sum((Decimal(str(d.amount)) for r in rents for d in r.discounts),Decimal("0"))
    pending=max(total_rent-paid-discount,Decimal("0"))
    return {"total_tenants":len(tenants),"total_plans":len(plans),"total_rent":total_rent,"total_paid":paid,"total_discount":discount,"total_pending":pending}
