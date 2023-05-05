from fastapi import HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from schemas import UtilisateurOut
from crud import get_utilisateur_by_email
from typing import Optional

class LoginInput(BaseModel):
    email: str
    password: str

def authenticate_user(db: Session, email: str, password: str) -> Optional[UtilisateurOut]:
    user = get_utilisateur_by_email(db, email)
    if not user:
        return None
    if not user.verify_password(password):
        return None
    return user
