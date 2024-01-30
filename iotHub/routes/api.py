from app import app
from flask import jsonify, request
import json, requests

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
server_back_end_url = app.config['SERVER_BACK_END_URL']

@app.route('/api/iot-hub/put/qrCode', methods=['PUT'])
def receiveQrCodeData():
    
    if request.method == 'PUT':
        try:
            data = request.get_json()
            print('Je recois les données :')
            print(data)
            
            qrType = data['QrType']
            qrId = data['QrId']
            print(qrType)
            print(qrId)
            
            if qrType == 'Badge':
                end_point = "/api/scanne/badge"
            else:
                end_point = "/api/scanne/ticket"
            
            data = {
                'qrType': qrType,
                'qrId': qrId
            }
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
            print(str(e))
            return jsonify({
                "status": 500,
                "error": f"Erreur de réception des données coté serveur IOH-HUB. {str(e)}"
            }), 500
    response = {
        "status": 405,
        "error": "Vous devez utiliser une requête PUT pour cette route."
    }
    return jsonify(response), 405