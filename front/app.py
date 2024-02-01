"""
|
|   This file contains all configuration for the front-end of this application.
|
|   Author: Mahmoud ILLOURMANE
|   Date: December 15, 2023
|
"""

"""
|
| App Configurations
|
"""

from flask import Flask
import secrets
from datetime import timedelta

app = Flask(__name__)

# Configuration pour les vues
app.template_folder = 'resources'
# Configuration pour les fichiers statiques
app.static_folder = 'static'

# Génère une clé secrète aléatoire de 32 caractères (256 bits)
secret_key = secrets.token_hex(32)
# Utilise la clé secrète dans la configuration de l'application Flask
app.config['SECRET_KEY'] = secret_key

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Activation du mode de débogage
app.debug = True

# Configuration du serveur pour reload le contenu des pages web
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Configuration de l'url des serveurs
# En Local
app.config['SERVER_DOOR_URL'] = 'http://127.0.0.1:5002'
app.config['SERVER_BACK_END_URL'] = 'http://127.0.0.1:5001'
app.config['SERVER_FRONT_END_URL'] = 'http://127.0.0.1:5000'

# En VM
# app.config['SERVER_DOOR_URL'] = 'http://door:5000'
# app.config['SERVER_BACK_END_URL'] = 'http://server:5000'
# app.config['SERVER_FRONT_END_URL'] = 'http://front:5000'

# Importations des fichier web.py et api.py
from routes.api import *
from routes.web import *

if __name__ == '__main__':
    # En Vm & En Local
    app.run(host='0.0.0.0', port=5000)

