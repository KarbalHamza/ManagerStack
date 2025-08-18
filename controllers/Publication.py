from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from Models.Publication import Publication
from database import get_db
from typing import List, Dict

router = APIRouter(
    prefix="/api/publications",
    tags=["PUBLICATIONS"],
    responses={404: {"description": "Non trouvé"}}
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_publication(
    contenu: str,
    date_publication: str,
    compte_id: int,
    db: Session = Depends(get_db)
) -> Dict:
    """Crée une nouvelle publication"""
    try:
        new_publication = Publication(
            Contenu=contenu,
            DatePublication=date_publication,
            ID_Compte=compte_id
        )
        db.add(new_publication)
        db.commit()
        db.refresh(new_publication)
        return {
            "status": "success",
            "data": new_publication
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur de création: {str(e)}"
        )

@router.get("/", response_model=List[Dict])
async def get_all_publications(db: Session = Depends(get_db)) -> List[Dict]:
    """Liste toutes les publications"""
    publications = db.query(Publication).all()
    return [{
        "id": pub.ID_Publication,
        "contenu": pub.Contenu,
        "date_publication": pub.DatePublication,
        "compte_id": pub.ID_Compte
    } for pub in publications]

@router.get("/{pub_id}")
async def get_publication(
    pub_id: int,
    db: Session = Depends(get_db)
) -> Dict:
    """Récupère une publication spécifique"""
    publication = db.query(Publication).filter(Publication.ID_Publication == pub_id).first()
    if not publication:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publication non trouvée"
        )
    return publication

@router.put("/{pub_id}")
async def update_publication(
    pub_id: int,
    contenu: str,
    date_publication: str,
    db: Session = Depends(get_db)
) -> Dict:
    """Met à jour une publication existante"""
    publication = db.query(Publication).filter(Publication.ID_Publication == pub_id).first()
    if not publication:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publication non trouvée"
        )
    
    try:
        publication.Contenu = contenu
        publication.DatePublication = date_publication
        db.commit()
        db.refresh(publication)
        return publication
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur de mise à jour: {str(e)}"
        )

@router.delete("/{pub_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_publication(
    pub_id: int,
    db: Session = Depends(get_db)
):
    publication = db.query(Publication).filter(Publication.ID_Publication == pub_id).first()
    if not publication:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publication non trouvée"
        )
    
    try:
        db.delete(publication)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur de suppression: {str(e)}"
        )
    
    # J'ai supprimé tout return explicite