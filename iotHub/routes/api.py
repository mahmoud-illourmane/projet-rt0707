
from flask import jsonify, request
import json, requests

# subscriber.py
import asyncio
from aiocoap import *

"""
|
|   This file contains the REST API of the IOT-HUB.
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

server_back_end_url = 'http://127.0.0.1:5001'
server_door_url = 'http://127.0.0.1:5002'

async def send_coap_message():
    protocol = await Context.create_client_context()

    request = Message(code=POST, payload=b'OK', uri=f"coap://{server_door_url}/resource")
    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to send CoAP message:', e)
    else:
        print('Message sent to publisher:', response.payload)

def sendQrCodeInfosToServer(qrCodeInfos:json):
    api_url = f"{server_back_end_url}/api/iot-hub/put/qrCode"
    
    qrType = qrCodeInfos['QrType']
    qrId = qrCodeInfos['QrId']

    print('qrcode id: ', qrId)
    print('qrcode type: ', qrType)
        
    print('Envoi des données.')
        
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

    # Envoi de la requête PUT
    try:
        api_url = f"{server_back_end_url}{end_point}"

        response = requests.put(api_url, json=data)
        response.raise_for_status()
        print('Données envoyé.')
            
        if response.status_code == 200:
            response = {
                "status": 200,
                "message": "Porte Ouverte."
            }
            print(response) 
            return jsonify(response), 200
        else:
            print(response)
            response = {
                "status": 400,
                "message": "Impossible d'ouvrir la porte."
            }
            return jsonify(response), 400
    except Exception as e:
        error_message = f"Erreur de requête vers l'URL distante brokerMqTT: {str(e)}"
        return {
            "status": 500, 
            "error": error_message
        }, 500