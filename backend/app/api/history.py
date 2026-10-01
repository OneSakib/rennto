from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.tenant import Tenant
from app.models.rent import Rent, Payment, Discount

router=APIRouter()

def tenant_history(db,tenant):
    items=[]
    for r in tenant.rents:
        items.append({"type":"rent","id":r.id,"date":r.due_date,"amount":r.amount,"billing_month":r.billing_month,"description":"Monthly rent generated"})
        for p in r.payments:
            items.append({"type":"payment","id":p.id,"date":p.payment_date,"amount":p.amount,"billing_month":r.billing_month,"description":f"Payment via {p.payment_method}","notes":p.notes})
        for d in r.discounts:
            items.append({"type":"discount","id":d.id,"date":d.created_at.date(),"amount":d.amount,"billing_month":r.billing_month,"description":"Discount / waiver","notes":d.reason})
    return sorted(items,key=lambda x:(x["date"],x["id"]),reverse=True)

@router.get("")
def global_history(db:Session=Depends(get_db), user=Depends(get_current_user)):
    tenants=db.query(Tenant).filter(Tenant.user_id==user.id).all()
    result=[]
    for t in tenants:
        for item in tenant_history(db,t):
            result.append({"tenant_id":t.id,"tenant_name":t.name,**item})
    return sorted(result,key=lambda x:(x["date"],x["id"]),reverse=True)

@router.get("/tenant/{tenant_id}")
def tenant_history_endpoint(tenant_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    tenant=db.query(Tenant).filter(Tenant.id==tenant_id,Tenant.user_id==user.id).first()
    if not tenant: raise HTTPException(404,"Tenant not found")
    return {"tenant":{"id":tenant.id,"name":tenant.name,"phone":tenant.phone,"property_name":tenant.property_name},"history":tenant_history(db,tenant)}
