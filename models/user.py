from sqlalchemy import Column, Integer, String, Date
from database import Base

# Modèle de la table "Utilisateurs"
class User(Base):
    __tablename__ = "Utilisateurs"

    ID_utilisateur = Column(Integer, primary_key=True)
    Nom_utilisateur = Column(String(255))
    Email = Column(String(255))
    Mot_de_passe = Column(String(255))
    Date_inscription = Column(Date)
