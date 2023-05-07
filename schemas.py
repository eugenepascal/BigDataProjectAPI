from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from datetime import date
import re

class UtilisateurBase(BaseModel):
    Nom_utilisateur: str
    Email: str
    Mot_de_passe: str

class UtilisateurCreate(UtilisateurBase):
    Date_inscription: Optional[date] = None

    @validator("Mot_de_passe")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Le mot de passe doit comporter au moins 8 caractères.")
        return value

    @validator("Email")
    def validate_email(cls, value):
        pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not pattern.match(value):
            raise ValueError("Email invalide.")
        return value

class UtilisateurUpdate(BaseModel):
    Nom_utilisateur: Optional[str] = None
    Email: Optional[str] = None
    Mot_de_passe: Optional[str] = None
    Date_inscription: Optional[date] = None

class UtilisateurOut(UtilisateurBase):
    ID_utilisateur: int

    class Config:
        orm_mode = True

class LoginInput(BaseModel):
    Nom_utilisateur: str
    Mot_de_passe: str

class ResetPasswordInput(BaseModel):
    Email: EmailStr
    new_password: str

class UserLogged(UtilisateurBase):
    ID_utilisateur: int
    Date_inscription: date
