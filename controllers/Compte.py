from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.compte import Compte
from schemas.compte_schema import CompteCreate, CompteOut

router = APIRouter(prefix="/comptes", tags=["Comptes"])

@router.post("/", response_model=CompteOut)
def create_compte(compte: CompteCreate, db: Session = Depends(get_db)):
    new_compte = Compte(**compte.dict())
    db.add(new_compte)
    db.commit()
    db.refresh(new_compte)
    return new_compte

@router.get("/", response_model=list[CompteOut])
def get_comptes(db: Session = Depends(get_db)):
    return db.query(Compte).all()

@router.get("/{compte_id}", response_model=CompteOut)
def get_compte(compte_id: int, db: Session = Depends(get_db)):
    compte = db.query(Compte).get(compte_id)
    if not compte:
        raise HTTPException(status_code=404, detail="Compte not found")
    return compte

@router.put("/{compte_id}", response_model=CompteOut)
def update_compte(compte_id: int, update: CompteCreate, db: Session = Depends(get_db)):
    compte = db.query(Compte).get(compte_id)
    if not compte:
        raise HTTPException(status_code=404, detail="Compte not found")
    for key, value in update.dict().items():
        setattr(compte, key, value)
    db.commit()
    db.refresh(compte)
    return compte

@router.delete("/{compte_id}")
def delete_compte(compte_id: int, db: Session = Depends(get_db)):
    compte = db.query(Compte).get(compte_id)
    if not compte:
        raise HTTPException(status_code=404, detail="Compte not found")
    db.delete(compte)
    db.commit()
    return {"message": "Compte deleted"}
