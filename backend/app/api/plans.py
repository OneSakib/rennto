from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.plan import Plan
from app.schemas.common import PlanCreate, PlanOut

router=APIRouter()

@router.get("", response_model=list[PlanOut])
def list_plans(db:Session=Depends(get_db), user=Depends(get_current_user)):
    return db.query(Plan).filter(Plan.user_id==user.id).order_by(Plan.id.desc()).all()

@router.post("", response_model=PlanOut)
def create_plan(data:PlanCreate, db:Session=Depends(get_db), user=Depends(get_current_user)):
    if not 1 <= data.due_day <= 28:
        raise HTTPException(400,"Due day must be between 1 and 28")
    plan=Plan(user_id=user.id,**data.model_dump())
    db.add(plan); db.commit(); db.refresh(plan); return plan

@router.get("/{plan_id}", response_model=PlanOut)
def get_plan(plan_id:int, db:Session=Depends(get_db), user=Depends(get_current_user)):
    plan=db.query(Plan).filter(Plan.id==plan_id,Plan.user_id==user.id).first()
    if not plan: raise HTTPException(404,"Plan not found")
    return plan

@router.delete("/{plan_id}")
def delete_plan(plan_id:int, db:Session=Depends(get_db), user=Depends(get_current_user)):
    plan=db.query(Plan).filter(Plan.id==plan_id,Plan.user_id==user.id).first()
    if not plan: raise HTTPException(404,"Plan not found")
    plan.status=False; db.commit(); return {"message":"Plan deactivated"}
