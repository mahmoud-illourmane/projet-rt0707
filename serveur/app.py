from flask import Flask

"""
|
|   Ce fichier constitue le point d'amorçage du serveur 
|   Flask pour l'API REST principale du projet.
|
|   Auteur: Mahmoud ILLOURMANE
|   Date de création: 18 Janvier 2024
|
"""

app = Flask(__name__)

# Activation du mode de débogage
app.debug = True                                                                

"""
|
|   Configuration des adresses IPs des différents serveurs
|
"""
# En VM
# app.config['SERVER_FRONT_END_URL'] = 'http://front:5000'

# En Local
app.config['SERVER_FRONT_END_URL'] = 'http://127.0.0.1:5000'

"""
|
|   Configuration des variables d'environnement pour la connexion MongoDB
|
"""
DATABASE_NAME = "projetRt0707"

# En VM
# MONGO_USERNAME = 'mongoadmin'
# MONGO_PASSWORD = 'secret'
# MONGO_HOSTNAME = 'mongo'
# MONGO_PORT = 27017
# MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOSTNAME}:{MONGO_PORT}"

# --------------
# En local
MONGO_URI = f"mongodb://localhost:27017"

# Importation du fichier api.py
from routes.api import *

if __name__ == '__main__':
    # En Vm
    # app.run(host='0.0.0.0', port=5000)
    
    # En Local
    app.run(host='0.0.0.0', port=5001)