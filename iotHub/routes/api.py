from flask import jsonify
from app import app
import json, requests, threading

import asyncio
from aiocoap import *

from src.classes.tools import write_log

"""
|
|   This file contains the REST API of the IOT-HUB.
|
|   Author: Mahmoud ILLOURMANE
|   Date: December 30, 2024
|
"""

server_back_end_url = app.config.get('SERVER_BACK_END_URL')

#
#   Méthodes CoAP
#

async def send_coap_message(uri="coap://door/resource", payload=b'OK'):
    protocol = await Context.create_client_context()
    request = Message(code=POST, payload=payload, uri=uri)
    try:
        response = await protocol.request(request).response
        # print('Message sent to door:', response.payload)
        write_log(f"Message sent to door: {response.payload}")
    except Exception as e:
        write_log(f"Failed to send CoAP message: {str(e)}")
        print('Failed to send CoAP message:', e)

def run_async_coap(uri, payload):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_coap_message(uri, payload))
        
#
#   Méthodes Requests
#

def sendQrCodeInfosToServer(qrCodeInfos:json):
    qrType = qrCodeInfos['QrType']
    qrId = qrCodeInfos['QrId']

    write_log(f"qrcode id: {qrId}")
    write_log(f"qrcode type: {qrType}")
    write_log("Envoi des données.")
        
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
            threading.Thread(target=lambda: run_async_coap("coap://door/resource", b'OK'), daemon=True).start()
            response = {
                "status": 200,
                "message": "Porte Ouverte."
            }
            return jsonify(response), 200
        else:
            threading.Thread(target=lambda: run_async_coap("coap://door/resource", b'KO'), daemon=True).start()
            response = {
                "status": 400,
                "message": "Impossible d'ouvrir la porte."
            }
            return jsonify(response), 400
    except Exception as e:
        error_message = f"Erreur de requête vers l'URL distante IOTHUB: {str(e)}"
        write_log(error_message)
        return {
            "status": 500, 
            "error": error_message
        }, 500