import json, requests

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

server_iot_hub_url = 'http://127.0.0.1:5004'

def sendQrCodeInfosToServer(qrCodeInfos:json):
    api_url = f"{server_iot_hub_url}/api/iot-hub/put/qrCode"
    
    try:
        print(qrCodeInfos)
        print('Envoi des données.')
        response = requests.put(api_url, json=qrCodeInfos)
        response.raise_for_status()
        
        if response.status_code  == 200:
            print("IOT-HUB a bien reçu les données")
        else:
            print("Erreur coté serveur distant IOT-HUB")

    except Exception as e:
        error_message = f"Erreur de requête vers l'URL distante brokerMqTT: {str(e)}"
        return {
            "status": 500, 
            "error": error_message
        }, 500