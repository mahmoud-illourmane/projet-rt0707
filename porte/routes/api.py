from app import app          
from flask import jsonify, request
import json

from src.classes.qrCode import QRCode
from mqtt.publisher import MQTTClient
from src.classes.verif import Verif

"""
|
|   This file contains the REST API of the door simulation routes for the project.
|
|   Author: Mahmoud ILLOURMANE
|   Date: December 30, 2024
|
"""

"""
|   ===============
|   API REST ROUTES
|   ===============
"""

# Initialisation de l'instance du client MQTT
mqtt_client = MQTTClient(client_id="PythonPublisher")

@app.route('/door/publish', methods=['POST'])
def publish_message():
    """
        Route pour publier un message via MQTT à la réception d'une requête HTTP POST.
    """
    
    data = request.json  # Obtention des données JSON de la requête
    qrCode = data['qrCodeBase64']

    qrCodeInfos = QRCode.decode_json_from_qr_code(qrCode)
    
    result = Verif.qrCodeVerifLocal(qrCodeInfos)
    if not result:
        response = {
            'status': 405,
            'error': 'Votre titre de transport est périmé.'
        }
        return jsonify(response), 200
    
    topic = "check/transport"
    message = {
        'QrId': qrCodeInfos['id'],
        'QrType': qrCodeInfos['type'],
    }

    if topic and message:
        # Publication du message sur le topic spécifié
        mqtt_client.publish(topic, json.dumps(message))
        print('PORTE: données publiées.')
        return jsonify({
            'status': 200, 
            'message': "Porte Ouverte pendant 3sc"
        }), 200
    else:
        return jsonify({
            'success': 500,
            'error': "Topic et/ou message manquants"
        }), 200
