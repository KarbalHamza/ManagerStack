from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from Models.user import User
from database import get_db
from typing import List, Dict

router = APIRouter(
    prefix="/api/users",
    tags=["USERS"],
    responses={404: {"description": "Non trouvé"}}
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    username: str,
    email: str,
    password: str,
    db: Session = Depends(get_db)
) -> Dict:
    """Crée un nouvel utilisateur"""
    try:
        # Vérifie si l'utilisateur existe déjà
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email déjà utilisé"
            )

        new_user = User(
            username=username,
            email=email,
            password=password  # Note: Dans la pratique, hashé le mot de passe
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "status": "success",
            "data": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur de création: {str(e)}"
        )

@router.get("/", response_model=List[Dict])
async def get_all_users(db: Session = Depends(get_db)) -> List[Dict]:
    """Liste tous les utilisateurs (sans mots de passe)"""
    users = db.query(User).all()
    return [{
        "id": user.id,
        "username": user.username,
        "email": user.email
    } for user in users]

@router.get("/{user_id}")
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
) -> Dict:
    """Récupère un utilisateur spécifique"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }

@router.put("/{user_id}")
async def update_user(
    user_id: int,
    username: str,
    email: str,
    db: Session = Depends(get_db)
) -> Dict:
    """Met à jour un utilisateur existant"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    try:
        user.username = username
        user.email = email
        db.commit()
        db.refresh(user)
        return {
            "status": "success",
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur de mise à jour: {str(e)}"
        )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    try:
        db.delete(user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur de suppression: {str(e)}"
        )