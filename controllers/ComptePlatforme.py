from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.compteplateforme import ComptePlateforme
from schemas.compteplateforme_schema import ComptePlateformeCreate, ComptePlateformeOut

router = APIRouter(prefix="/compteplateformes", tags=["ComptePlateforme"])

@router.post("/", response_model=ComptePlateformeOut)
def create_compteplateforme(relation: ComptePlateformeCreate, db: Session = Depends(get_db)):
    new_relation = ComptePlateforme(**relation.dict())
    db.add(new_relation)
    db.commit()
    db.refresh(new_relation)
    return new_relation

@router.get("/", response_model=list[ComptePlateformeOut])
def get_all_relations(db: Session = Depends(get_db)):
    return db.query(ComptePlateforme).all()

# 👁️ Voir une relation par ID
@router.get("/{relation_id}", response_model=ComptePlateformeOut)
def get_relation(relation_id: int, db: Session = Depends(get_db)):
    relation = db.query(ComptePlateforme).get(relation_id)
    if not relation:
        raise HTTPException(status_code=404, detail="Relation not found")
    return relation

@router.put("/{relation_id}", response_model=ComptePlateformeOut)
def update_relation(relation_id: int, update: ComptePlateformeCreate, db: Session = Depends(get_db)):
    relation = db.query(ComptePlateforme).get(relation_id)
    if not relation:
        raise HTTPException(status_code=404, detail="Relation not found")
    for key, value in update.dict().items():
        setattr(relation, key, value)
    db.commit()
    db.refresh(relation)
    return relation

@router.delete("/{relation_id}")
def delete_relation(relation_id: int, db: Session = Depends(get_db)):
    relation = db.query(ComptePlateforme).get(relation_id)
    if not relation:
        raise HTTPException(status_code=404, detail="Relation not found")
    db.delete(relation)
    db.commit()
    return {"message": "Relation supprimée"}
