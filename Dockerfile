# Utiliser une image de base Python 3.9 avec slim-buster
FROM python:3.9-slim-buster

# Créer un répertoire pour l'application et le définir comme répertoire de travail
RUN mkdir /app
WORKDIR /app

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers de l'application dans le répertoire de travail
COPY . .

# Exposer le port 8000 pour l'API
#EXPOSE 8000

# Démarrer l'API avec uvicorn
#CMD ["uvicorn", "main:app", "--port", "8000", "--reload"]
CMD uvicorn main:app --reload --host 0.0.0.0
EXPOSE 8000
