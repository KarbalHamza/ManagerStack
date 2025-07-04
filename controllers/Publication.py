from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.publication import Publication
from schemas.publication_schema import PublicationCreate, PublicationOut

router = APIRouter(prefix="/publications", tags=["Publications"])

@router.post("/", response_model=PublicationOut)
def create_publication(pub: PublicationCreate, db: Session = Depends(get_db)):
    new_pub = Publication(**pub.dict())
    db.add(new_pub)
    db.commit()
    db.refresh(new_pub)
    return new_pub

@router.get("/", response_model=list[PublicationOut])
def get_all_publications(db: Session = Depends(get_db)):
    return db.query(Publication).all()

@router.get("/{pub_id}", response_model=PublicationOut)
def get_publication(pub_id: int, db: Session = Depends(get_db)):
    pub = db.query(Publication).get(pub_id)
    if not pub:
        raise HTTPException(status_code=404, detail="Publication non trouvée")
    return pub

@router.put("/{pub_id}", response_model=PublicationOut)
def update_publication(pub_id: int, updated: PublicationCreate, db: Session = Depends(get_db)):
    pub = db.query(Publication).get(pub_id)
    if not pub:
        raise HTTPException(status_code=404, detail="Publication non trouvée")
    for key, value in updated.dict().items():
        setattr(pub, key, value)
    db.commit()
    db.refresh(pub)
    return pub

@router.delete("/{pub_id}")
def delete_publication(pub_id: int, db: Session = Depends(get_db)):
    pub = db.query(Publication).get(pub_id)
    if not pub:
        raise HTTPException(status_code=404, detail="Publication non trouvée")
    db.delete(pub)
    db.commit()
    return {"message": "Publication supprimée"}
