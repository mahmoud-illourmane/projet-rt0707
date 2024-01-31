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

@app.route('/door/publish', methods=['PUT'])
def publish_message():
    """
        Route pour publier un message via MQTT à la réception d'une requête HTTP PUT.
    """
    
    data = request.json  # Obtention des données JSON de la requête
    qrCode = data['qrCodeBase64']

    qrCodeInfos = QRCode.decode_json_from_qr_code(qrCode)
    
    # Vérifications en local du titre de transport
    result = Verif.qrCodeVerifLocal(qrCodeInfos)
    if not result:
        response = {
            'status': 405,
            'error': 'PORTE: Votre titre de transport est périmé.'
        }
        return jsonify(response), 200
    
    # Préparation de la Topic pour publication
    topic = "check/transport"
    message = {
        'QrId': qrCodeInfos['id'],
        'QrType': qrCodeInfos['type'],
    }

    # Publication de la topic dans la file MqTT
    if topic and message:
        mqtt_client.publish(topic, json.dumps(message))
        print('PORTE: données publiées.')
        return jsonify({
            'status': 200, 
            'message': "Porte Ouverte pendant 3sc MESSAGE FORGE A LA MAIN !"
        }), 200
    else:
        return jsonify({
            'success': 500,
            'error': "Topic et/ou message manquants"
        }), 200
