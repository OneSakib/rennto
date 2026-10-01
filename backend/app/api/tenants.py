from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.tenant import Tenant
from app.models.plan import TenantPlan, Plan
from app.models.rent import Rent, Payment, Discount
from app.schemas.common import TenantCreate, TenantOut, AssignPlan

router = APIRouter()

def owned_tenant(db, user, tenant_id):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id, Tenant.user_id == user.id).first()
    if not tenant: raise HTTPException(404, "Tenant not found")
    return tenant

@router.get("", response_model=list[TenantOut])
def list_tenants(db: Session=Depends(get_db), user=Depends(get_current_user)):
    return db.query(Tenant).filter(Tenant.user_id == user.id).order_by(Tenant.id.desc()).all()

@router.post("", response_model=TenantOut)
def create_tenant(data: TenantCreate, db: Session=Depends(get_db), user=Depends(get_current_user)):
    tenant = Tenant(user_id=user.id, **data.model_dump())
    db.add(tenant); db.commit(); db.refresh(tenant)
    return tenant

@router.get("/{tenant_id}", response_model=TenantOut)
def get_tenant(tenant_id:int, db:Session=Depends(get_db), user=Depends(get_current_user)):
    return owned_tenant(db,user,tenant_id)

@router.patch("/{tenant_id}", response_model=TenantOut)
def update_tenant(tenant_id:int, data:TenantCreate, db:Session=Depends(get_db), user=Depends(get_current_user)):
    tenant=owned_tenant(db,user,tenant_id)
    for k,v in data.model_dump().items(): setattr(tenant,k,v)
    db.commit(); db.refresh(tenant); return tenant

@router.delete("/{tenant_id}")
def delete_tenant(tenant_id:int, db:Session=Depends(get_db), user=Depends(get_current_user)):
    tenant=owned_tenant(db,user,tenant_id)
    db.delete(tenant); db.commit()
    return {"message":"Tenant deleted"}

@router.post("/{tenant_id}/plans")
def assign_plan(tenant_id:int, data:AssignPlan, db:Session=Depends(get_db), user=Depends(get_current_user)):
    tenant=owned_tenant(db,user,tenant_id)
    plan=db.query(Plan).filter(Plan.id==data.plan_id, Plan.user_id==user.id, Plan.status==True).first()
    if not plan: raise HTTPException(404,"Plan not found")
    current=db.query(TenantPlan).filter(TenantPlan.tenant_id==tenant.id,TenantPlan.status==True).first()
    if current:
        current.status=False
        current.end_date=data.start_date
    tp=TenantPlan(tenant_id=tenant.id,plan_id=plan.id,start_date=data.start_date,status=True)
    db.add(tp); db.commit(); db.refresh(tp)
    return {"id":tp.id,"tenant_id":tenant.id,"plan_id":plan.id,"message":"Plan assigned"}
