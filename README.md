# API-projetBigData

Nous avons implémenté une API pour faciliter les interactions entre l'application de quiz et notre base de données.
L' API a été construite avec FastAPI un cadre web moderne, rapide (hautes performances) et facile à utiliser, pour construire des API avec Python 3.6+ basé 
sur les types de notation standard.

# Avantages de FastAPI
FastAPI a de nombreux avantages qui en font un excellent choix pour notre API  :

Performance : FastAPI est l'un des frameworks Python les plus rapides disponibles, sur par avec NodeJS et Go.

Facilité d'utilisation : FastAPI est facile à utiliser et à comprendre. Il est également entièrement compatible avec les éditeurs de code modernes, offrant l'autocomplétion et la vérification de type.

Validation automatique des requêtes : FastAPI utilise Pydantic pour la validation automatique des requêtes, ce qui réduit la quantité de code nécessaire pour valider les entrées et facilite la détection et la gestion des erreurs.

Documentation automatique : FastAPI génère automatiquement une documentation d'API interactive à l'aide de Swagger. Cela facilite le test de l'API et permet de comprendre rapidement et facilement le fonctionnement de l'API.

Support pour les WebSockets et les GraphQL : FastAPI pccccrend en charge les WebSockets pour des connexions en temps réel entre le client et le serveur, et GraphQL pour des requêtes plus efficaces.

# Cadre d'utilisation de l'API

L'API joue un rôle crucial en fournissant une série de points de terminaison qui permettent à l'application 
de quiz de réaliser une variété de tâches, notamment :

Gestion des utilisateurs : L'API offre des points de terminaison pour créer, récupérer, mettre à jour et supprimer des utilisateurs. Cela permet à l'application de quiz de gérer efficacement les utilisateurs, de suivre leur progression, de stocker leurs scores et d'offrir une expérience personnalisée.

Gestion des questions de quiz : L'API permet également de gérer les questions de quiz. Cela comprend l'ajout de nouvelles questions, la récupération de questions existantes, la mise à jour de questions et la suppression de questions. Cela permet à l'application de quiz de proposer un large éventail de questions, de suivre lesquelles ont été posées à chaque utilisateur et de mettre à jour les questions au fil du temps.

Authentification et sécurité : L'API comprend également des points de terminaison pour l'authentification des utilisateurs. Cela permet à l'application de quiz de s'assurer que seuls les utilisateurs autorisés ont accès à certaines fonctionnalités, de protéger les informations des utilisateurs et de prévenir les utilisations abusives.

Scoring et leaderboards : En gardant une trace des scores des utilisateurs et en fournissant des points de terminaison pour récupérer les scores les plus élevés, l'API permet à l'application de quiz de maintenir des tableaux de classement dynamiques et de promouvoir une saine compétition entre les utilisateurs.

Intégration du modèle de reconnaissance vocale pour le déroulement du quizz où les utilisateurs répondent à la voix.

# Configuration de l'API
    Les informations de configuration, notamment les informations d'authentification de la base de données, sont stockées dans un fichier .env


# Installation des dépendances 

Pour installer les dépendances nécessaires, il faut ouvrir un terminal, naviguer jusqu'au répertoire contenant le fichier requirements.txt
Et exécuter la commande suivante :

    pip install -r requirements.txt

# Lancement de l'API
Pour démarrer l'API, il faut naviguer jusqu'au répertoire contenant le fichier main.py et exécuter  ensuite la commande suivante :

    uvicorn main:app --reload

Cette commande lancera un serveur de développement local sur votre machine. Vous pouvez accéder à l'API en ouvrant votre navigateur web et en naviguant jusqu'à http://localhost:8000.


# Déploiement de l'API dans le cloud Azure

 ----- Prérequis

    Compte Azure : Nous avons utilisé un compte gratuit
    Azure CLI : Azure CLI est une interface de ligne de commande pour interagir avec les services Azure.
    Docker : Docker est utilisé pour construire une image Docker de notre API.

---- Les étapes de déploiement :

Construire l'image Docker : Dans notre terminal, on construit l'image Docker en utilisant la commande suivante 
#  
       docker build -t quizzgame .

Connexion à l'interface d'Azure en ligne de commande : avec az login

Création d'un groupe de ressources : Un groupe de ressources est un conteneur logique pour les ressources déployées sur Azure

Création d'un registre de conteneurs Azure : Un registre de conteneurs est un endroit pour stocker et gérer les images de conteneurs pour le déploiement de Docker

Connexion au registre Docker :

Tag de l'image :

Déploiement de l'image dans le registre : pour cela il faut créer une instance d'application sur Azure pour pouvoir déployer le conteneur

Configuration des paramètres de l'application : Dans cette partie, il faut configurer les paramètres nécessaires pour pouvoir accéder à notre application

Navigation dans l'application : on peut naviguer dans l'application en ouvrant un navigateur web et en accédant à l'URL de l'application fournie.










     
















