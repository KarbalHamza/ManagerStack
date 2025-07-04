from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.planning import Planning
from schemas.planning_schema import PlanningCreate, PlanningOut

router = APIRouter(prefix="/plannings", tags=["Plannings"])

@router.post("/", response_model=PlanningOut)
def create_planning(planning: PlanningCreate, db: Session = Depends(get_db)):
    new_planning = Planning(**planning.dict())
    db.add(new_planning)
    db.commit()
    db.refresh(new_planning)
    return new_planning

@router.get("/", response_model=list[PlanningOut])
def get_all_plannings(db: Session = Depends(get_db)):
    return db.query(Planning).all()

@router.get("/{planning_id}", response_model=PlanningOut)
def get_planning(planning_id: int, db: Session = Depends(get_db)):
    planning = db.query(Planning).get(planning_id)
    if not planning:
        raise HTTPException(status_code=404, detail="Planning not found")
    return planning

@router.put("/{planning_id}", response_model=PlanningOut)
def update_planning(planning_id: int, update: PlanningCreate, db: Session = Depends(get_db)):
    planning = db.query(Planning).get(planning_id)
    if not planning:
        raise HTTPException(status_code=404, detail="Planning not found")
    for key, value in update.dict().items():
        setattr(planning, key, value)
    db.commit()
    db.refresh(planning)
    return planning

@router.delete("/{planning_id}")
def delete_planning(planning_id: int, db: Session = Depends(get_db)):
    planning = db.query(Planning).get(planning_id)
    if not planning:
        raise HTTPException(status_code=404, detail="Planning not found")
    db.delete(planning)
    db.commit()
    return {"message": "Planning supprimé"}
