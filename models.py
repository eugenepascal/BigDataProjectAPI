from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Utilisateur(Base):
    __tablename__ = "Utilisateurs"

    ID_utilisateur = Column(Integer, primary_key=True, index=True)
    Nom_utilisateur = Column(String(255), nullable=False)
    Email = Column(String(255), nullable=False)
    Mot_de_passe = Column(String(255), nullable=False)
    Date_inscription = Column(Date, nullable=True)
