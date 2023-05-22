from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from typing import List
import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette import status
from torch.autograd import Variable
import torchaudio
import torch
import numpy as np
import io

from schemas import UtilisateurCreate, UtilisateurOut, GameCreate
from crud import get_utilisateur, create_utilisateur, delete_utilisateur, get_all_utilisateurs
from database import SessionLocal
from schemas import LoginInput, ResetPasswordInput, UserLogged
from crud import authenticate_user, reset_password
from model_cnn import CNN
from Azure import upload_to_azure_storage

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

valid_sentences = ['deux', 'non', 'oui', 'quatre', 'trois', 'un']

model = CNN()
model.load_state_dict(torch.load('model_state_dict.pt'))
model.eval()


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
async def get_all_users(skip: int = 0, limit: int = 100,):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utilisateurs;")
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return rows

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

@app.post("/game", response_model=UtilisateurOut)
async def insert_game(game: GameCreate):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Générer un ID_utilisateur unique pour le nouvel utilisateur
    cursor.execute("SELECT MAX(ID_Partie) FROM Utilisateurs")
    max_id = cursor.fetchone()[0]
    new_id = max_id + 1 if max_id is not None else 1

    # Insérer le nouvel utilisateur dans la base de données
    cursor.execute(
        f"INSERT INTO parties (ID_partie, ID_utilisateur, ID_Categorie, Difficulte,"
        f" Nombre_questions, Type_questions, Pourcentage_reussite, Date_partie) "
        f"VALUES ({new_id}, '{game.ID_utilisateur}', '{game.ID_Categorie}', '{game.Difficulte}', '{game.Nombre_questions}'"
        f", '{game.Type_questions}', '{game.Pourcentage_reussite}', '{game.Date_partie}')"
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

@app.post("/upload")
async def upload_audio_file(audio: UploadFile = File(...)):
    upload_to_azure_storage(audio)
    return {"detail": "Audio file uploaded successfully"}



@app.post("/predict/")
async def predict_audio(file: UploadFile = File(...)):
    # Load the audio file
    blob = await file.read()
    sound, sample_rate = torchaudio.load(io.BytesIO(blob))

    # Padding
    max_length = 48000  # You might need to adjust this value
    if sound.shape[1] < max_length:
        padding = torch.zeros(1, max_length - sound.shape[1])
        sound = torch.cat([sound, padding], dim=1)

    # MelSpectrogram
    specgram = torchaudio.transforms.MelSpectrogram(sample_rate, n_fft=1024, n_mels=64)(sound)
    specgram = torchaudio.transforms.AmplitudeToDB(top_db=80)(specgram)

    # Adding batch dimension
    specgram = specgram.unsqueeze(0)

    # Pass through the model
    outputs = model(specgram)
    _, predicted = torch.max(outputs.data, 1)
    return {"prediction": valid_sentences[predicted.item()]}

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