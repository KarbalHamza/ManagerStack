from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from Models.ComptePlatforme import ComptePlateforme
from database import get_db
from typing import List, Dict

router = APIRouter(
    prefix="/api/compteplateformes",
    tags=["COMPTE_PLATEFORMES"],
    responses={404: {"description": "Non trouvé"}}
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_compte_plateforme(
    compte_id: int,
    plateforme_id: int,
    db: Session = Depends(get_db)
) -> Dict:
    """Crée une nouvelle relation compte-plateforme"""
    try:
        new_relation = ComptePlateforme(
            ID_Compte=compte_id,
            ID_Plateforme=plateforme_id
        )
        db.add(new_relation)
        db.commit()
        db.refresh(new_relation)
        return {
            "status": "success",
            "data": new_relation
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur de création: {str(e)}"
        )

@router.get("/", response_model=List[Dict])
async def get_all_relations(db: Session = Depends(get_db)) -> List[Dict]:
    """Liste toutes les relations compte-plateforme"""
    relations = db.query(ComptePlateforme).all()
    return [{
        "id": rel.ID,
        "compte_id": rel.ID_Compte,
        "plateforme_id": rel.ID_Plateforme
    } for rel in relations]

@router.get("/{relation_id}")
async def get_relation(
    relation_id: int,
    db: Session = Depends(get_db)
) -> Dict:
    """Récupère une relation spécifique"""
    relation = db.query(ComptePlateforme).filter(ComptePlateforme.ID == relation_id).first()
    if not relation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relation non trouvée"
        )
    return relation

@router.put("/{relation_id}")
async def update_relation(
    relation_id: int,
    compte_id: int,
    plateforme_id: int,
    db: Session = Depends(get_db)
) -> Dict:
    """Met à jour une relation existante"""
    relation = db.query(ComptePlateforme).filter(ComptePlateforme.ID == relation_id).first()
    if not relation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relation non trouvée"
        )
    
    try:
        relation.ID_Compte = compte_id
        relation.ID_Plateforme = plateforme_id
        db.commit()
        db.refresh(relation)
        return relation
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur de mise à jour: {str(e)}"
        )

@router.delete("/{relation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_relation(
    relation_id: int,
    db: Session = Depends(get_db)
):
    """Supprime une relation"""
    relation = db.query(ComptePlateforme).filter(ComptePlateforme.ID == relation_id).first()
    if not relation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relation non trouvée"
        )

    try:
        db.delete(relation)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur de suppression: {str(e)}"
        )