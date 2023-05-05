from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from models import Utilisateur
from schemas import UtilisateurCreate, UtilisateurUpdate
from crud import create_utilisateur, update_utilisateur, delete_utilisateur

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/utilisateurs/", response_model=UtilisateurCreate)
def ajouter_utilisateur(utilisateur: UtilisateurCreate, db: Session = Depends(get_db)):
    return create_utilisateur(db, utilisateur)


@router.put("/utilisateurs/{utilisateur_id}/", response_model=UtilisateurCreate)
def modifier_utilisateur(utilisateur_id: int, utilisateur: UtilisateurUpdate, db: Session = Depends(get_db)):
    db_utilisateur = update_utilisateur(db, utilisateur_id, utilisateur)
    if db_utilisateur is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return db_utilisateur


@router.delete("/utilisateurs/{utilisateur_id}/", response_model=UtilisateurCreate)
def supprimer_utilisateur(utilisateur_id: int, db: Session = Depends(get_db)):
    db_utilisateur = delete_utilisateur(db, utilisateur_id)
    if db_utilisateur is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return db_utilisateur
