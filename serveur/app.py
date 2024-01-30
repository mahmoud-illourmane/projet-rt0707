"""
|
|   This file contains all the configuration settings for the server API REST of the project.
|
|   Author: Mahmoud ILLOURMANE
|   Date: January 18, 2024
|
|
"""

# Importation des packages nécessaires au bon fonctionnement du projet Flask
from flask import Flask

"""
|
| App Configurations
|
"""

app = Flask(__name__)
# Activation du mode de débogage
app.debug = True

app.config['SERVER_FRONT_END_URL'] = 'http://front:5000'

# Récupération des variables d'environnement pour la connexion MongoDB en mode VM
MONGO_USERNAME = 'mongoadmin'
MONGO_PASSWORD = 'secret'
MONGO_HOSTNAME = 'mongo'
MONGO_PORT = 27017

# Utilisation de l'adresse du service Docker MongoDB comme URI
MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOSTNAME}:{MONGO_PORT}"
DATABASE_NAME = "projetRt0707"

# Importation du fichier api.py
from routes.api import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)