"""
|
|   This file contains all the configuration settings for the server of the project.
|
|   Author: Mahmoud ILLOURMANE
|   Date: January 18, 2024
|
|
"""

# Importation des packages nécessaires au bon fonctionnement du projet Flask
from flask import Flask
import os


"""
|
| App Configurations
|
"""

app = Flask(__name__)

# Activation du mode de débogage
app.debug = True

# Récupération des variables d'environnement pour la connexion MongoDB
MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_HOSTNAME = os.environ.get('MONGO_HOSTNAME')
MONGO_PORT = os.environ.get('MONGO_PORT')

# Configuration de la connexion à MongoDB
MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOSTNAME}:{MONGO_PORT}/"
DATABASE_NAME = "projetRt0707"


# Initialisation et utilisation de la connexion MongoDB
# with MongoDBManager(MONGO_URI, DATABASE_NAME) as db_manager:
    # users_collection = db_manager.get_collection('users')
    
# Importation du fichier api.py
from routes.api import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)