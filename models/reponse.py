from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Modèle de la table "Réponses"
class Reponse(Base):
    __tablename__ = "Réponses"

    ID_reponse = Column(Integer, primary_key=True)
    ID_question = Column(Integer, ForeignKey('Questions.ID_question'))
    Réponse_texte = Column(String(255))
    Est_correcte = Column(Boolean)
    question = relationship("Question", backref="reponses")
