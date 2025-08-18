from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from Models.profil import Profil
from database import get_db
from typing import List, Dict

router = APIRouter(
    prefix="/api/profils",
    tags=["PROFILS"],
    responses={404: {"description": "Non trouvé"}}
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_profil(
    nom_profil: str,
    description: str,
    compte_id: int,
    db: Session = Depends(get_db)
) -> Dict:
    """Crée un nouveau profil"""
    try:
        new_profil = Profil(
            NomProfil=nom_profil,
            Description=description,
            ID_Compte=compte_id
        )
        db.add(new_profil)
        db.commit()
        db.refresh(new_profil)
        return {
            "status": "success",
            "data": {
                "id": new_profil.ID_Profil,
                "nom": new_profil.NomProfil,
                "description": new_profil.Description,
                "compte_id": new_profil.ID_Compte
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur de création: {str(e)}"
        )

@router.get("/", response_model=List[Dict])
async def get_all_profils(db: Session = Depends(get_db)) -> List[Dict]:
    """Liste tous les profils"""
    profils = db.query(Profil).all()
    return [{
        "id": profil.ID_Profil,
        "nom": profil.NomProfil,
        "description": profil.Description,
        "compte_id": profil.ID_Compte
    } for profil in profils]

@router.get("/{profil_id}")
async def get_profil(
    profil_id: int,
    db: Session = Depends(get_db)
) -> Dict:
    """Récupère un profil spécifique"""
    profil = db.query(Profil).filter(Profil.ID_Profil == profil_id).first()
    if not profil:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil non trouvé"
        )
    return profil

@router.put("/{profil_id}")
async def update_profil(
    profil_id: int,
    nom_profil: str,
    description: str,
    db: Session = Depends(get_db)
) -> Dict:
    """Met à jour un profil existant"""
    profil = db.query(Profil).filter(Profil.ID_Profil == profil_id).first()
    if not profil:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil non trouvé"
        )
    
    try:
        profil.NomProfil = nom_profil
        profil.Description = description
        db.commit()
        db.refresh(profil)
        return profil
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur de mise à jour: {str(e)}"
        )

@router.delete("/{profil_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profil(
    profil_id: int,
    db: Session = Depends(get_db)
):
    profil = db.query(Profil).filter(Profil.ID_Profil == profil_id).first()
    if not profil:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil non trouvé"
        )
    
    try:
        db.delete(profil)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur de suppression: {str(e)}"
        )