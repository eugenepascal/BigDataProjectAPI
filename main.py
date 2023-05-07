from fastapi import FastAPI, HTTPException, Depends
from typing import List
import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette import status

from schemas import UtilisateurCreate, UtilisateurOut
from crud import get_utilisateur, create_utilisateur, delete_utilisateur, get_all_utilisateurs
from database import SessionLocal
from schemas import LoginInput, ResetPasswordInput, UserLogged
from crud import authenticate_user, reset_password

# Charger les valeurs du fichier .env
load_dotenv()

# Récupérer les informations de connexion de la base de données à partir du fichier .env
mysql_user = os.getenv("DB_USER")
mysql_password = os.getenv("DB_PASSWORD")
mysql_host = os.getenv("DB_HOST")
mysql_database = os.getenv("DB_NAME")

config = {
  'host':mysql_host,
  'user':mysql_user,
  'password':mysql_password,
  'database':mysql_database,
}

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def test_connection():
    try:
        conn = mysql.connector.connect(**config)
        print("Successfully connected to the database.")
        conn.close()
        return True
    except Exception as e:
        print(f"Error in test_connection: {e}")  # Afficher l'erreur pour aider au débogage
        return False


@app.on_event("startup")
async def startup():
    if not test_connection():
        raise HTTPException(status_code=500, detail="Could not connect to database")

def get_db():
    db = SessionLocal()
    db.commit()
    return db

@app.get("/")
async def read_root():
    return {"message": "Successfully connected to Azure MySQL database!"}

@app.get("/utilisateurs")
async def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utilisateurs;")
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return rows#users#get_all_utilisateurs(db, skip=skip, limit=limit)

@app.post("/utilisateurs/", response_model=UtilisateurOut)
async def create_user(user: UtilisateurCreate):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Générer un ID_utilisateur unique pour le nouvel utilisateur
    cursor.execute("SELECT MAX(ID_utilisateur) FROM Utilisateurs")
    max_id = cursor.fetchone()[0]
    new_id = max_id + 1 if max_id is not None else 1

    # Insérer le nouvel utilisateur dans la base de données
    cursor.execute(
        f"INSERT INTO Utilisateurs (ID_utilisateur, Nom_utilisateur, Email, Mot_de_passe, Date_inscription) "
        f"VALUES ({new_id}, '{user.Nom_utilisateur}', '{user.Email}', '{user.Mot_de_passe}', '{user.Date_inscription}')"
    )

    conn.commit()
    cursor.close()
    conn.close()

    # Retourner le nouvel utilisateur créé
    return {
        "ID_utilisateur": new_id,
        "Nom_utilisateur": user.Nom_utilisateur,
        "Email": user.Email,
        "Mot_de_passe": user.Mot_de_passe,
        "Date_inscription": user.Date_inscription,
    }


@app.get("/utilisateurs/{user_id}", response_model=UtilisateurOut)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_utilisateur(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/utilisateurs/{user_id}")
async def remove_user(user_id: int, db: Session = Depends(get_db)):
    user = get_utilisateur(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    delete_utilisateur(db, user_id)
    return {"message": f"User {user_id} deleted successfully"}

@app.post("/login", response_model=UserLogged)
async def login_route(login_input: LoginInput):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utilisateurs WHERE Nom_utilisateur = %s;", (login_input.Nom_utilisateur,))
    user = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    print(user[0])
    if user is None or user[3] != login_input.Mot_de_passe:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nom_utilisateur ou mot de passe incorrect")
    return {
        "ID_utilisateur": user[0],
        "Nom_utilisateur": user[1],
        "Email": user[2],
        "Mot_de_passe": user[3],
        "Date_inscription": user[4],
    }

@app.post("/reset-password")
async def reset_password_route(reset_input: ResetPasswordInput):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utilisateurs WHERE Email = %s;", (reset_input.Email,))
    user = cursor.fetchone()

    if user is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")

    cursor.execute("UPDATE utilisateurs SET Mot_de_passe = %s WHERE Email = %s;", (reset_input.new_password, reset_input.Email))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Password reset successfully"}