from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.profil import Profil
from schemas.profil_schema import ProfilCreate, ProfilOut

router = APIRouter(prefix="/profils", tags=["Profils"])

@router.post("/", response_model=ProfilOut)
def create_profil(profil: ProfilCreate, db: Session = Depends(get_db)):
    new_profil = Profil(**profil.dict())
    db.add(new_profil)
    db.commit()
    db.refresh(new_profil)
    return new_profil

@router.get("/", response_model=list[ProfilOut])
def get_profils(db: Session = Depends(get_db)):
    return db.query(Profil).all()

@router.get("/{profil_id}", response_model=ProfilOut)
def get_profil(profil_id: int, db: Session = Depends(get_db)):
    profil = db.query(Profil).get(profil_id)
    if not profil:
        raise HTTPException(status_code=404, detail="Profil not found")
    return profil

@router.put("/{profil_id}", response_model=ProfilOut)
def update_profil(profil_id: int, update: ProfilCreate, db: Session = Depends(get_db)):
    profil = db.query(Profil).get(profil_id)
    if not profil:
        raise HTTPException(status_code=404, detail="Profil not found")
    for key, value in update.dict().items():
        setattr(profil, key, value)
    db.commit()
    db.refresh(profil)
    return profil

@router.delete("/{profil_id}")
def delete_profil(profil_id: int, db: Session = Depends(get_db)):
    profil = db.query(Profil).get(profil_id)
    if not profil:
        raise HTTPException(status_code=404, detail="Profil not found")
    db.delete(profil)
    db.commit()
    return {"message": "Profil supprimé"}
