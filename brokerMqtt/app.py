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
from mqtt.subscriber import MQTTSubscriber

"""
|
| App Configurations
|
"""

app = Flask(__name__)
# Activation du mode de débogage
app.debug = True

# Configuration des l'urls des différents serveurs
app.config['SERVER_IOT_HUB_URL'] = 'http://127.0.0.1:5004'

# Importation du fichier api.py
from routes.api import *

if __name__ == '__main__':
    # Ici, je démarre le subscriber MQTT en parallèle de Flask
    subscriber = MQTTSubscriber()
    subscriber.start()
    app.run(host='0.0.0.0', port=5003)
    