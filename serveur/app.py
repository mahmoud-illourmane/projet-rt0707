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
from config.database import *
from pymongo import MongoClient

"""
|
| App Configurations
|
"""

app = Flask(__name__)

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["projet"]
users = db["users"]

# Données de l'utilisateur à insérer
utilisateur = {
    "nom": "John Doe",
    "email": "john.doe@example.com",
    "age": 30
}

# Insertion dans la collection 'users'
resultat = users.insert_one(utilisateur)
print("Utilisateur inséré avec l'ID :", resultat.inserted_id)

# Activation du mode de débogage
app.debug = True

# Importation du fichier api.py
from routes.api import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
