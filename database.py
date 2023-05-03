from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Charger les valeurs du fichier .env
from dotenv import load_dotenv
load_dotenv()

# Récupérer les informations de connexion de la base de données à partir du fichier .env
mysql_user = os.getenv("DB_USER")
mysql_password = os.getenv("DB_PASSWORD")
mysql_host = os.getenv("DB_IP")
mysql_database = os.getenv("DB_NAME")

# Création de la chaîne de connexion
connection_string = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:3306/{mysql_database}"

# Création du moteur SQLAlchemy
engine = create_engine(connection_string)

# Création de la Session SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
