from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from Models.Platforme import Plateforme
from database import get_db
from typing import List, Dict

router = APIRouter(
    prefix="/api/plateformes",
    tags=["PLATEFORMES"],
    responses={404: {"description": "Non trouvé"}}
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_plateforme(
    nom: str,
    url: str,
    type_plateforme: str,
    db: Session = Depends(get_db)
) -> Dict:
    """Crée une nouvelle plateforme"""
    try:
        new_plateforme = Plateforme(
            NomPlateforme=nom,
            URL=url,
            TypePlateforme=type_plateforme
        )
        db.add(new_plateforme)
        db.commit()
        db.refresh(new_plateforme)
        return {
            "status": "success",
            "data": new_plateforme
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur de création: {str(e)}"
        )

@router.get("/", response_model=List[Dict])
async def get_all_plateformes(db: Session = Depends(get_db)) -> List[Dict]:
    """Liste toutes les plateformes"""
    plateformes = db.query(Plateforme).all()
    return [{
        "id": plateforme.ID_Plateforme,
        "nom": plateforme.NomPlateforme,
        "url": plateforme.URL,
        "type": plateforme.TypePlateforme
    } for plateforme in plateformes]

@router.get("/{plateforme_id}")
async def get_plateforme(
    plateforme_id: int,
    db: Session = Depends(get_db)
) -> Dict:
    """Récupère une plateforme spécifique"""
    plateforme = db.query(Plateforme).filter(Plateforme.ID_Plateforme == plateforme_id).first()
    if not plateforme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plateforme non trouvée"
        )
    return plateforme

@router.put("/{plateforme_id}")
async def update_plateforme(
    plateforme_id: int,
    nom: str,
    url: str,
    type_plateforme: str,
    db: Session = Depends(get_db)
) -> Dict:
    """Met à jour une plateforme existante"""
    plateforme = db.query(Plateforme).filter(Plateforme.ID_Plateforme == plateforme_id).first()
    if not plateforme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plateforme non trouvée"
        )
    
    try:
        plateforme.NomPlateforme = nom
        plateforme.URL = url
        plateforme.TypePlateforme = type_plateforme
        db.commit()
        db.refresh(plateforme)
        return plateforme
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur de mise à jour: {str(e)}"
        )
@router.delete("/{plateforme_id}")  # Pas de status_code=204
async def delete_plateforme(
    plateforme_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    plateforme = db.query(Plateforme).filter(Plateforme.ID_Plateforme == plateforme_id).first()
    if not plateforme:
        raise HTTPException(status_code=404, detail="Plateforme non trouvée")
    
    try:
        db.delete(plateforme)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")
    
    return {"message": "Plateforme supprimée avec succès"}  # Retourne un JSON