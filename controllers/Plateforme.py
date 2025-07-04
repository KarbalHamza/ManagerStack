from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.plateforme import Plateforme
from schemas.plateforme_schema import PlateformeCreate, PlateformeOut

router = APIRouter(prefix="/plateformes", tags=["Plateformes"])

# ➕ Créer une plateforme
@router.post("/", response_model=PlateformeOut)
def create_plateforme(plateforme: PlateformeCreate, db: Session = Depends(get_db)):
    new_plateforme = Plateforme(**plateforme.dict())
    db.add(new_plateforme)
    db.commit()
    db.refresh(new_plateforme)
    return new_plateforme

# 📄 Voir toutes les plateformes
@router.get("/", response_model=list[PlateformeOut])
def get_plateformes(db: Session = Depends(get_db)):
    return db.query(Plateforme).all()

# 👁️ Voir une plateforme par ID
@router.get("/{plateforme_id}", response_model=PlateformeOut)
def get_plateforme(plateforme_id: int, db: Session = Depends(get_db)):
    plateforme = db.query(Plateforme).get(plateforme_id)
    if not plateforme:
        raise HTTPException(status_code=404, detail="Plateforme not found")
    return plateforme

# ✏️ Modifier une plateforme
@router.put("/{plateforme_id}", response_model=PlateformeOut)
def update_plateforme(plateforme_id: int, update: PlateformeCreate, db: Session = Depends(get_db)):
    plateforme = db.query(Plateforme).get(plateforme_id)
    if not plateforme:
        raise HTTPException(status_code=404, detail="Plateforme not found")
    for key, value in update.dict().items():
        setattr(plateforme, key, value)
    db.commit()
    db.refresh(plateforme)
    return plateforme

# ❌ Supprimer une plateforme
@router.delete("/{plateforme_id}")
def delete_plateforme(plateforme_id: int, db: Session = Depends(get_db)):
    plateforme = db.query(Plateforme).get(plateforme_id)
    if not plateforme:
        raise HTTPException(status_code=404, detail="Plateforme not found")
    db.delete(plateforme)
    db.commit()
    return {"message": "Plateforme supprimée"}
