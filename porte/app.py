"""
|
|   This file contains all the configuration settings for the DOOR simulation.
|
|   Author: Mahmoud ILLOURMANE
|   Date: January 26, 2024
|
"""

from flask import Flask, request, jsonify

# Imports pour le fonctionnement de CoAP
import asyncio
from aiocoap import *
from aiocoap.resource import Resource, Site

# Import de threading pour lancer le serveur CoAP en Parralèle de Flask
import threading, json, time
from queue import Queue, Empty

# Imports de Classes Personnelles
from mqtt.publisher import MQTTClient
from src.classes.qrCode import QRCode
from src.classes.verif import Verif
from src.classes.tools import write_log

# Déclaration de la file d'attente pour permettre des échanges entre CoAP et Flask
response_queue = Queue()

app = Flask(__name__)
app.debug = True

"""
|
|   Classes pour gérer le serveur CoAP
|
"""

class SimpleResource(Resource):
    """
        Classe représentant une ressource simple pour le serveur CoAP.
                
        Methodes:
            async def render_post(self, request): Méthode asynchrone pour gérer les requêtes POST CoAP.
    """
    
    async def render_post(self, request):
        """
            Méthode asynchrone pour gérer les requêtes POST CoAP.

            Args:
                request (Request): L'objet requête CoAP.

            Returns:
                Message: Un objet Message CoAP en réponse à la requête.
        """
        
        payload = request.payload.decode('utf-8')                             # Récupération du payload
        write_log(f"PORTE : Requête COAP RECU : {payload},")
                               
        if payload == 'OK':                                                   # Vérification de la valeur du payload pour débogage
            write_log("SERVEUR COAP : ECRIT DANS LA FILE OK.")
            response_queue.put('OK')                                          # Place la réponse dans la queue       
            write_log(f"SERVEUR COAP A ECRIT DANS LA FILE : {payload}")
        elif payload == 'KO':
            write_log("SERVEUR COAP : ECRIT DANS LA FILE KO.")
            response_queue.put('KO')
            write_log(f"SERVEUR COAP A ECRIT DANS LA FILE : {payload}")

class CoAPServer:
    """
        Classe représentant un serveur CoAP.

        Attributes:
            loop (asyncio.BaseEventLoop): La boucle d'événements asyncio utilisée par le serveur.

        Methodes:
            async def start_server(self): Méthode asynchrone pour démarrer le serveur CoAP.
            def run(self): Méthode pour exécuter le serveur CoAP en utilisant la boucle d'événements asyncio.
    """

    def __init__(self):
        """
            Initialise un nouvel objet CoAPServer avec une nouvelle boucle d'événements asyncio.
        """
        self.loop = asyncio.new_event_loop()

    async def start_server(self):
        """
            Méthode asynchrone pour démarrer le serveur CoAP.
            Crée un contexte de serveur pour le serveur CoAP avec une SimpleResource comme ressource.
        """
        root = Site()                                                          # Crée le serveur CoAP ici
        root.add_resource(['resource'], SimpleResource())                      # Ajoute la SimpleResource au serveur CoAP
        await Context.create_server_context(root)                              # Crée un contexte de serveur pour le serveur CoAP

    def run(self):
        """
            Méthode pour exécuter le serveur CoAP en utilisant la boucle d'événements asyncio.
            Configure la boucle d'événements asyncio pour cette instance et démarre le serveur CoAP.
            Cette méthode s'exécute en continu pour maintenir le serveur actif.
        """
        asyncio.set_event_loop(self.loop)                                      # Configure la boucle d'événements asyncio pour cette instance
        self.loop.run_until_complete(self.start_server())                      # Démarre le serveur CoAP en utilisant la boucle d'événements asyncio
        self.loop.run_forever()                                                # Exécute en continu la boucle d'événements asyncio pour maintenir le serveur actif

def start_coap_server():
    """
        Fonction qui démarre le serveur CoAP en créant une 
        instance de la classe CoAPServer et en exécutant sa méthode run().
    """
    server = CoAPServer()                                                      # Crée une instance de la classe CoAPServer
    server.run()                                                               # Lance le serveur CoAP en exécutant sa méthode run()

"""
|
|   Partie pour gérer la publication de topics
|   Dans la file MQTT.
|
"""
mqtt_client = MQTTClient("PythonPublisher")

"""
|
|   Routes Flask
|
"""

@app.route('/door/publish', methods=['PUT'])
def publish_message():
    """
        Route pour publier un message via MQTT à la réception d'une requête HTTP PUT du client.
    """
    
    if request.method == 'PUT':
        write_log("PORTE : Je reçois une demande de scan.")
        
        """
        |   PARTIE 1
        |   L'utilisateur souhaite scanner un titre de transport
        |   Réception de la requête HTTP PUT
        """
        
        # Obtention des données JSON
        data = request.json  
        # Extraction du QRCODE sous forme base64
        qrCode = data['qrCodeBase64']
        # Extraction des données du json
        qrCodeInfos = QRCode.decode_json_from_qr_code(qrCode)
        
        """
        |   PARTIE 2
        |   Le dispositif vérifie en local si la date de validité
        |   du titre n'est pas dépassé.
        """
        result = Verif.qrCodeVerifLocal(qrCodeInfos)
        if not result:
            write_log("PORTE: Votre titre de transport est périmé.")
            return jsonify({
                'status': 405,
                'error': 'PORTE: Votre titre de transport est périmé.'
            }), 200 # J'utilise 200, car je n'arrive pas à afficher les messages personnalisés dans la requête Ajax dans la section 'error'.
        
        """
        |   PARTIE 3
        |   Le dispositif publie l'id et le type du QRCODE dans la topic MQTT
        """
        topic = "check/transport"
        message = {
            'QrId': qrCodeInfos['id'],
            'QrType': qrCodeInfos['type'],
        }
        # Utilisation de la méthode de classe publish de MQTTClient
        mqtt_client.publish(topic, json.dumps(message))
        
        """
        |   PARTIE 4
        |   Après que le dispositif ait envoyé la topic, il doit attendre la réponse de
        |   l'IOT-HUB via une requête CoAP, avant de renvoyer la réponse de la requête HTTP
        |   de la PARTIE 1.
        """
        
        # J'attends que la réponse CoAP soit mise dans la file d'attente pour renvoyer la réponse au client
        try:
            write_log(f"PORTE : Nombre d'éléments dans la file avant extraction de la réponse : {response_queue.qsize()}")
            coap_response = response_queue.get(timeout=5) 
        except Empty:
            write_log("PORTE: ERREUR : Exception Empty, La PORTE a été bloqué plus de 5 secondes dans la file d'attente.")
            return jsonify({
                'status': 500,
                'error': 'La durée d\'attente de 5 secondes est écoulée, erreur (file d\'attente).'
            }), 200

        """
        |   PARTIE 5
        |   Après que le dispositif ait la réponse CoAP il répond à la requête HTTP de l'utilisateur.
        """
        write_log(f"PORTE : DONNEE EXTRAITE DEPUIS LA FILE D'ATTENTE.")
        if coap_response == 'OK':
            write_log(f"PORTE: Requête CoAP reçue : {coap_response}")
            return jsonify({
                'status': 200,
                'message': "Porte Ouverte pendant 3sc MESSAGE COAP!"
            }), 200
        elif coap_response == 'KO':
            write_log(f"PORTE: Requête CoAP reçue : {coap_response}")
            return jsonify({
                'status': 400,
                'error': "Porte fermée MESSAGE COAP!"
            }), 200
        else:
            write_log(f"PORTE: Requête CoAP reçue : INCONNUE")
            return jsonify({
                'status': 500,
                'error': 'Received unclear CoAP response'
            }), 200
            
    response = {
        "status": 405,
        "error": "Vous devez utiliser une requête PUT pour cette route."
    }
    return jsonify(response), 200

if __name__ == '__main__':
    # Démarrer le serveur CoAP dans un thread séparé
    coap_thread = threading.Thread(target=start_coap_server, daemon=True)
    coap_thread.start()

    # Démarrer l'application Flask sur le thread principal
    
    # En Vm
    app.run(host='0.0.0.0', port=5000)
    # En Local
    # app.run(host='0.0.0.0', port=5003)