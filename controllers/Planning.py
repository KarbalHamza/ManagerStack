from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from Models.Planning import Planning
from database import get_db
from typing import List, Dict

router = APIRouter(
    prefix="/api/plannings",
    tags=["PLANNINGS"],
    responses={404: {"description": "Non trouvé"}}
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_planning(
    date_publication: str,
    heure_publication: str,
    compte_id: int,
    db: Session = Depends(get_db)
) -> Dict:
    """Crée un nouveau planning"""
    try:
        new_planning = Planning(
            DatePublication=date_publication,
            HeurePublication=heure_publication,
            ID_Compte=compte_id
        )
        db.add(new_planning)
        db.commit()
        db.refresh(new_planning)
        return {
            "status": "success",
            "data": new_planning
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur de création: {str(e)}"
        )

@router.get("/", response_model=List[Dict])
async def get_all_plannings(db: Session = Depends(get_db)) -> List[Dict]:
    """Liste tous les plannings"""
    plannings = db.query(Planning).all()
    return [{
        "id": planning.ID_Planning,
        "date_publication": planning.DatePublication,
        "heure_publication": planning.HeurePublication,
        "compte_id": planning.ID_Compte
    } for planning in plannings]

@router.get("/{planning_id}")
async def get_planning(
    planning_id: int,
    db: Session = Depends(get_db)
) -> Dict:
    """Récupère un planning spécifique"""
    planning = db.query(Planning).filter(Planning.ID_Planning == planning_id).first()
    if not planning:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Planning non trouvé"
        )
    return planning

@router.put("/{planning_id}")
async def update_planning(
    planning_id: int,
    date_publication: str,
    heure_publication: str,
    db: Session = Depends(get_db)
) -> Dict:
    """Met à jour un planning existant"""
    planning = db.query(Planning).filter(Planning.ID_Planning == planning_id).first()
    if not planning:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Planning non trouvé"
        )
    
    try:
        planning.DatePublication = date_publication
        planning.HeurePublication = heure_publication
        db.commit()
        db.refresh(planning)
        return planning
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur de mise à jour: {str(e)}"
        )

@router.delete("/{planning_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_planning(
    planning_id: int,
    db: Session = Depends(get_db)
):
    planning = db.query(Planning).filter(Planning.ID_Planning == planning_id).first()
    if not planning:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Planning non trouvé"
        )
    
    try:
        db.delete(planning)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur de suppression: {str(e)}"
        ) 