from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from dotenv import load_dotenv
import os

from database import engine  # Importez 'engine' depuis 'database.py'

# Charger les valeurs du fichier .env
load_dotenv()

app = FastAPI()

@app.on_event("startup")
async def startup():
    try:
        # Test de la connexion à la base de données
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception as e:
        print(f"Error: {e}")  # Afficher l'erreur pour aider au débogage
        raise HTTPException(status_code=500, detail="Could not connect to database")

@app.get("/")
async def read_root():
    return {"message": "Successfully connected to Azure MySQL database!"}
