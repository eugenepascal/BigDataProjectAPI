from typing import Optional
from pydantic import BaseModel
from datetime import date


class UtilisateurBase(BaseModel):
    Nom_utilisateur: str
    Email: str
    Mot_de_passe: str


class UtilisateurCreate(UtilisateurBase):
    Date_inscription: Optional[date] = None


class UtilisateurUpdate(BaseModel):
    Nom_utilisateur: Optional[str] = None
    Email: Optional[str] = None
    Mot_de_passe: Optional[str] = None
    Date_inscription: Optional[date] = None


class UtilisateurOut(UtilisateurBase):
    ID_utilisateur: int

    class Config:
        orm_mode = True
