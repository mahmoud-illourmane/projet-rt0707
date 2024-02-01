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
import paho.mqtt.client as mqtt
import json, requests, threading

# Utiliser pour la requête CoAP
import asyncio
from aiocoap import *

# Utiliser pour les logs
from src.classes.tools import write_log

# FLASK
app = Flask(__name__)
app.debug = True     # Activation du mode de débogage

# En Vm
app.config['SERVER_BACK_END_URL'] = 'http://server:5000'
# En Local
# app.config['SERVER_BACK_END_URL'] = 'http://127.0.0.1:5001'

server_back_end_url = app.config.get('SERVER_BACK_END_URL')

"""
|
|   PARTIE MQTT
|
"""
class MQTTSubscriber:
    def __init__(self, app):
        """
            Constructeur de la classe MQTTSubscriber.

            Initialise un client MQTT avec un nom "PythonSubscriber", configure les méthodes de rappel
            et active le logging pour le débogage.
        """

        self.app = app
        self.client = mqtt.Client("PythonSubscriber")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.enable_logger()

    def on_connect(self, client, userdata, flags, rc):
        """
            Méthode de rappel appelée lors de la connexion à un broker MQTT.

            :param client: Objet client MQTT.
            :param userdata: Données utilisateur (optionnel).
            :param flags: Drapeaux de connexion (optionnel).
            :param rc: Code de retour de la connexion (0 si la connexion réussie).
        """
        
        if rc == 0:
            # write_log("Connecté avec succès au broker MQTT")
            client.subscribe("check/transport")
        else:
            write_log(f"Échec de la connexion avec le code {rc}")

    def on_message(self, client, userdata, msg):
        """
            Méthode de rappel appelée lors de la réception d'un message MQTT.

            :param client: Objet client MQTT.
            :param userdata: Données utilisateur (optionnel).
            :param msg: Objet message contenant le topic et le payload du message reçu.
        """
        
        write_log(f"Message reçu -> Topic: {msg.topic}, Payload: {msg.payload}")
        try:
            qrCodeInfos = json.loads(msg.payload.decode('utf-8'))  # Assurez-vous de décoder le payload
            # Utiliser le contexte de l'application pour exécuter la fonction Flask
            with self.app.app_context():
                write_log("IOT HUB: Tentative d'appel de la fonction sendQrCodeInfosToServer.")
                sendQrCodeInfosToServer(qrCodeInfos)
        except json.JSONDecodeError:
            write_log(f"Erreur lors de la décodification du message: {msg.payload}")

    def start(self):
        """
            Méthode pour démarrer un abonné MQTT.

            Crée un client MQTT, configure les méthodes de rappel, active le logging pour le débogage,
            établit la connexion avec un broker MQTT local sur le port 1883, et démarre la boucle du client MQTT
            en arrière-plan pour la gestion des messages.
        """
        
        # Utilisation de connect_async pour une gestion non bloquante de la connexion
        self.client.connect_async("brokerMqtt", 1883, 60)
        self.client.loop_start()

"""
|
|   PARTIE CoAP
|
"""
async def send_coap_message(uri="coap://door/resource", payload=b'OK'):
    protocol = await Context.create_client_context()
    request = Message(code=POST, payload=payload, uri=uri)
    try:
        response = await protocol.request(request).response
        # print('Message sent to door:', response.payload)
        write_log(f"REQUETE COAP : Message envoyé au serveur PORTE COAP : {response.payload}.")
    except Exception as e:
        write_log(f"Failed to send CoAP message: {str(e)}")
        print('Failed to send CoAP message:', e)

def run_async_coap(uri, payload):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_coap_message(uri, payload))

"""
|
|   PARTIE REST
|
"""
def sendQrCodeInfosToServer(qrCodeInfos:json):
    """
        Cette méthode envoi les données du QRCODE à l'API REST
        Pour traitements.
    """
    
    qrType = qrCodeInfos['QrType']
    qrId = qrCodeInfos['QrId']

    write_log("IOT HUB: Envoi des données A L'API REST.")
        
    # Détermine quel endPoint coté serveur flask appeler
    if qrType == 'Badge':
        end_point = "/api/scanne/badge"
    else:
        end_point = "/api/scanne/ticket"
    
    # Forge les données
    data = {
        'qrType': qrType,
        'qrId': qrId
    }

    # Envoi de la requête PUT à l4API REST
    try:
        api_url = f"{server_back_end_url}{end_point}"

        response = requests.put(api_url, json=data)
        response.raise_for_status()
        write_log("IOT HUB : Données envoyées à l'API REST.")
            
        # Envoie de la requête CoAP à la porte
        if response.status_code == 200:
            write_log("IOT HUB : REPONSE RECU OK, Tentative d'envoie CoaP (OK).")
            threading.Thread(target=lambda: run_async_coap("coap://door/resource", b'OK'), daemon=True).start()
            write_log("IOT HUB : Tentative d'envoie CoaP (OK) FAITE.")
        else:
            write_log("IOT HUB : REPONSE RECU KO, Tentative d'envoie CoaP (KO).")
            threading.Thread(target=lambda: run_async_coap("coap://door/resource", b'KO'), daemon=True).start()
            write_log("IOT HUB : Tentative d'envoie CoaP (KO) FAITE.")
           
    except Exception as e:
        error_message = f"Erreur de requête vers l'URL distante IOTHUB: {str(e)}"
        write_log(error_message)

def start_mqtt_subscriber():
    subscriber = MQTTSubscriber(app)
    subscriber.start()

if __name__ == '__main__':
    # Créer et démarrer un thread pour le subscriber MQTT
    mqtt_thread = threading.Thread(target=start_mqtt_subscriber, daemon=True)
    mqtt_thread.start()
    
    # En Vm
    app.run(host='0.0.0.0', port=5000)
    
    # En local
    # app.run(host='0.0.0.0', port=5003)

    