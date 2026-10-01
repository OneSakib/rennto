from calendar import monthrange
from datetime import date
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.tenant import Tenant
from app.models.plan import TenantPlan, Plan
from app.models.rent import Rent, Payment, Discount
from app.schemas.common import RentOut, PaymentCreate, DiscountCreate

router=APIRouter()

def owned_rent(db,user,rent_id):
    rent=(db.query(Rent).join(Tenant).filter(Rent.id==rent_id,Tenant.user_id==user.id).first())
    if not rent: raise HTTPException(404,"Rent not found")
    return rent

def rent_summary(rent):
    paid=sum((Decimal(str(x.amount)) for x in rent.payments),Decimal("0"))
    discount=sum((Decimal(str(x.amount)) for x in rent.discounts),Decimal("0"))
    pending=max(Decimal(str(rent.amount))-paid-discount,Decimal("0"))
    return {"paid":paid,"discount":discount,"pending":pending}

@router.get("", response_model=list[RentOut])
def list_rents(month:str|None=None, db:Session=Depends(get_db), user=Depends(get_current_user)):
    q=db.query(Rent).join(Tenant).filter(Tenant.user_id==user.id)
    if month: q=q.filter(Rent.billing_month==month)
    return q.order_by(Rent.due_date.desc(),Rent.id.desc()).all()

@router.get("/{rent_id}")
def get_rent(rent_id:int, db:Session=Depends(get_db), user=Depends(get_current_user)):
    rent=owned_rent(db,user,rent_id); s=rent_summary(rent)
    return {"rent":RentOut.model_validate(rent),"summary":s,"payments":rent.payments,"discounts":rent.discounts}

@router.post("/{rent_id}/payments")
def add_payment(rent_id:int,data:PaymentCreate,db:Session=Depends(get_db),user=Depends(get_current_user)):
    rent=owned_rent(db,user,rent_id); s=rent_summary(rent)
    if data.amount<=0 or data.amount>s["pending"]: raise HTTPException(400,f"Payment must be > 0 and <= pending {s['pending']}")
    p=Payment(rent_id=rent.id,tenant_id=rent.tenant_id,**data.model_dump())
    db.add(p); db.commit(); db.refresh(p)
    return {"message":"Payment recorded","payment":p,"summary":rent_summary(rent)}

@router.post("/{rent_id}/discounts")
def add_discount(rent_id:int,data:DiscountCreate,db:Session=Depends(get_db),user=Depends(get_current_user)):
    rent=owned_rent(db,user,rent_id); s=rent_summary(rent)
    if data.amount<=0 or data.amount>s["pending"]: raise HTTPException(400,f"Discount must be > 0 and <= pending {s['pending']}")
    d=Discount(rent_id=rent.id,tenant_id=rent.tenant_id,**data.model_dump())
    db.add(d); db.commit(); db.refresh(d)
    return {"message":"Discount recorded","discount":d,"summary":rent_summary(rent)}

@router.post("/generate-monthly")
def generate_monthly(month:str|None=None, db:Session=Depends(get_db), user=Depends(get_current_user)):
    today=date.today()
    month=month or today.strftime("%Y-%m")
    y,m=map(int,month.split("-"))
    created=[]
    assignments=(db.query(TenantPlan).join(Tenant).join(Plan).filter(
        Tenant.user_id==user.id,Tenant.status==True,TenantPlan.status==True,Plan.status==True
    ).all())
    for tp in assignments:
        if tp.start_date.strftime("%Y-%m") > month: continue
        if tp.end_date and tp.end_date.strftime("%Y-%m") < month: continue
        if db.query(Rent).filter(Rent.tenant_id==tp.tenant_id,Rent.billing_month==month).first(): continue
        day=min(tp.plan.due_day,monthrange(y,m)[1])
        r=Rent(tenant_id=tp.tenant_id,plan_id=tp.plan_id,billing_month=month,due_date=date(y,m,day),amount=tp.plan.amount)
        db.add(r); created.append(r)
    db.commit()
    return {"month":month,"created":len(created)}
