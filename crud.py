from sqlalchemy.orm import Session
from models import Utilisateur
from schemas import UtilisateurCreate, UtilisateurUpdate

def get_all_utilisateurs(db: Session, skip: int = 0, limit: int = 100):
    try:
        print(f"Executing query with skip: {skip}, limit: {limit}")
        users = db.query(Utilisateur).offset(skip).limit(limit).all()
        print(f"Query result: {users}")
    except Exception as e:
        print(f"Error in get_all_utilisateurs: {e}")
        raise


def create_utilisateur(db: Session, utilisateur: UtilisateurCreate):
    db_utilisateur = Utilisateur(**utilisateur.dict())
    db.add(db_utilisateur)
    db.commit()
    db.refresh(db_utilisateur)
    return db_utilisateur


def get_utilisateur(db: Session, utilisateur_id: int):
    return db.query(Utilisateur).filter(Utilisateur.ID_utilisateur == utilisateur_id).first()


def update_utilisateur(db: Session, utilisateur_id: int, utilisateur: UtilisateurUpdate):
    db_utilisateur = get_utilisateur(db, utilisateur_id)
    if not db_utilisateur:
        return None

    for key, value in utilisateur.dict().items():
        if value is not None:
            setattr(db_utilisateur, key, value)

    db.commit()
    db.refresh(db_utilisateur)
    return db_utilisateur


def delete_utilisateur(db: Session, utilisateur_id: int):
    db_utilisateur = get_utilisateur(db, utilisateur_id)
    if not db_utilisateur:
        return None

    db.delete(db_utilisateur)
    db.commit()
    return db_utilisateur

def authenticate_user(db: Session, Nom_utilisateur: str, Mot_de_passe: str):
    user = db.query(Utilisateur).filter(Utilisateur.Nom_utilisateur == Nom_utilisateur).first()
    if user and user.Mot_de_passe == Mot_de_passe:
        return user
    return None

def reset_password(db: Session, Email: str, new_password: str):
    user = db.query(Utilisateur).filter(Utilisateur.Email == Email).first()
    if not user:
        return None
    user.Mot_de_passe = new_password
    db.commit()
    return user


def get_utilisateur_by_email(db: Session, email: str):
    return db.query(Utilisateur).filter(Utilisateur.Email == email).first()
