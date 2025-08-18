from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from Models.Compte import Compte
from database import get_db
from typing import Dict, Any

router = APIRouter(
    prefix="/comptes",
    tags=["Comptes"],
    responses={404: {"description": "Not found"}},
)

# CREATE
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_compte(compte_data: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        new_compte = Compte(
            Nom_Compte=compte_data["Nom_Compte"],
            Type_De_Compte=compte_data["Type_De_Compte"],
            ID_User=compte_data["ID_User"]
        )
        db.add(new_compte)
        db.commit()
        db.refresh(new_compte)
        return new_compte
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Champ manquant : {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur SQL : {str(e)}"
        )

# READ ALL
@router.get("/")
def get_comptes(db: Session = Depends(get_db)):
    return db.query(Compte).all()

# READ ONE
@router.get("/{compte_id}")
def get_compte(compte_id: int, db: Session = Depends(get_db)):
    compte = db.query(Compte).filter(Compte.ID_Compte == compte_id).first()
    if not compte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compte non trouvé"
        )
    return compte

# UPDATE
@router.put("/{compte_id}")
def update_compte(compte_id: int, compte_data: Dict[str, Any], db: Session = Depends(get_db)):
    compte = db.query(Compte).filter(Compte.ID_Compte == compte_id).first()
    if not compte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compte non trouvé"
        )
    
    try:
        if "Nom_Compte" in compte_data:
            compte.Nom_Compte = compte_data["Nom_Compte"]
        if "Type_De_Compte" in compte_data:
            compte.Type_De_Compte = compte_data["Type_De_Compte"]
        
        db.commit()
        db.refresh(compte)
        return compte
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur SQL : {str(e)}"
        )

# DELETE
@router.delete("/{compte_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_compte(compte_id: int, db: Session = Depends(get_db)):
    compte = db.query(Compte).filter(Compte.ID_Compte == compte_id).first()
    if not compte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compte non trouvé"
        )
    
    try:
        db.delete(compte)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur SQL : {str(e)}"
        )