from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.media import Media
from schemas.media_schema import MediaCreate, MediaOut

router = APIRouter(prefix="/medias", tags=["Medias"])

@router.post("/", response_model=MediaOut)
def create_media(media: MediaCreate, db: Session = Depends(get_db)):
    new_media = Media(**media.dict())
    db.add(new_media)
    db.commit()
    db.refresh(new_media)
    return new_media

@router.get("/", response_model=list[MediaOut])
def get_all_medias(db: Session = Depends(get_db)):
    return db.query(Media).all()

# 👁️ Voir un media par ID
@router.get("/{media_id}", response_model=MediaOut)
def get_media(media_id: int, db: Session = Depends(get_db)):
    media = db.query(Media).get(media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return media

@router.put("/{media_id}", response_model=MediaOut)
def update_media(media_id: int, update: MediaCreate, db: Session = Depends(get_db)):
    media = db.query(Media).get(media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    for key, value in update.dict().items():
        setattr(media, key, value)
    db.commit()
    db.refresh(media)
    return media

@router.delete("/{media_id}")
def delete_media(media_id: int, db: Session = Depends(get_db)):
    media = db.query(Media).get(media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    db.delete(media)
    db.commit()
    return {"message": "Media supprimé"}
