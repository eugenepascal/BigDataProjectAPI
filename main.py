from fastapi import FastAPI, HTTPException, Depends
from typing import List
import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from schemas import UtilisateurCreate, UtilisateurOut
from crud import get_utilisateur, create_utilisateur, delete_utilisateur, get_all_utilisateurs
from database import SessionLocal

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
async def create_user(user: UtilisateurCreate, db: Session = Depends(get_db)):
    return create_utilisateur(db, user)

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
