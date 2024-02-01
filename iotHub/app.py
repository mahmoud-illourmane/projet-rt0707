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

# Utiliser pour lancer en parallèle flask et mqtt
import threading    

app = Flask(__name__)
app.debug = True     # Activation du mode de débogage

# En Vm
# app.config['SERVER_BACK_END_URL'] = 'http://serveur:5000'
# En Local
app.config['SERVER_BACK_END_URL'] = 'http://127.0.0.1:5001'

# Importation du fichier api.py
from routes.api import *
from mqtt.subscriber import MQTTSubscriber

def start_mqtt_subscriber():
    subscriber = MQTTSubscriber(app)
    subscriber.start()

if __name__ == '__main__':
    # Créer et démarrer un thread pour le subscriber MQTT
    mqtt_thread = threading.Thread(target=start_mqtt_subscriber, daemon=True)
    mqtt_thread.start()
    
    # En Vm
    # app.run(host='0.0.0.0', port=5000)
    # En Local
    app.run(host='0.0.0.0', port=5003)
    