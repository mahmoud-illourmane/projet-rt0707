"""
|
|   This file contains all the configuration settings for the Broker MQTT.
|
|   Author: Mahmoud ILLOURMANE
|   Date: January 30, 2024
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

# Configuration des l'urls des différents serveurs
app.config['SERVER_BACK_END_URL'] = 'http://serveur:5000'

# Importation du fichier api.py
from routes.api import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    