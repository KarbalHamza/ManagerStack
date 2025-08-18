from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from Models.Media import Media
from database import get_db
from typing import List, Dict

router = APIRouter(
    prefix="/api/medias",
    tags=["MEDIAS"],
    responses={404: {"description": "Non trouvé"}}
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_media(
    url: str,
    type_media: str,
    compte_id: int,
    db: Session = Depends(get_db)
) -> Dict:
    """Crée un nouveau média"""
    try:
        new_media = Media(
            URL=url,
            TypeMedia=type_media,
            ID_Compte=compte_id
        )
        db.add(new_media)
        db.commit()
        db.refresh(new_media)
        return {
            "status": "success",
            "data": new_media
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur de création: {str(e)}"
        )

@router.get("/", response_model=List[Dict])
async def get_all_medias(db: Session = Depends(get_db)) -> List[Dict]:
    """Liste tous les médias"""
    medias = db.query(Media).all()
    return [{
        "id": media.ID_Media,
        "url": media.URL,
        "type": media.TypeMedia,
        "compte_id": media.ID_Compte
    } for media in medias]

@router.get("/{media_id}")
async def get_media(
    media_id: int,
    db: Session = Depends(get_db)
) -> Dict:
    """Récupère un média spécifique"""
    media = db.query(Media).filter(Media.ID_Media == media_id).first()
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Média non trouvé"
        )
    return media

@router.put("/{media_id}")
async def update_media(
    media_id: int,
    url: str,
    type_media: str,
    db: Session = Depends(get_db)
) -> Dict:
    """Met à jour un média existant"""
    media = db.query(Media).filter(Media.ID_Media == media_id).first()
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Média non trouvé"
        )
    
    try:
        media.URL = url
        media.TypeMedia = type_media
        db.commit()
        db.refresh(media)
        return media
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur de mise à jour: {str(e)}"
        )
    
@router.delete("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_media(
    media_id: int,
    db: Session = Depends(get_db)
):
    """Supprime un média"""
    media = db.query(Media).filter(Media.ID_Media == media_id).first()
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Média non trouvé"
        )
    
    try:
        db.delete(media)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur de suppression: {str(e)}"
        )