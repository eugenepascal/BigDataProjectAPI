from sqlalchemy import Column, Integer, String, Date, ForeignKey,
from sqlalchemy.orm import relationship
from database import Base

# Modèle de la table "Questions"
class Question(Base):
    __tablename__ = "Questions"

    ID_question = Column(Integer, primary_key=True)
    Question_texte = Column(String(255))
    ID_utilisateur = Column(Integer, ForeignKey('Utilisateurs.ID_utilisateur'))
    Difficulte = Column(Integer)
    Date_creation = Column(Date)
    utilisateur = relationship("User", backref="questions")
