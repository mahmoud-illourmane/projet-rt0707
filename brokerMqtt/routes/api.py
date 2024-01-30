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

server_back_end_url = 'http://127.0.0.1:5001'
server_door_url = 'http://127.0.0.1:5002'

def sendQrCodeInfosToServer(qrCodeInfos:json):
    qrType = qrCodeInfos['QrType']
    qrId = qrCodeInfos['QrId']
    print(qrType)
    print(qrId)
    
    if qrType == 'Badge':
        end_point = "/api/scanne/badge"
    else:
        end_point = "/api/scanne/ticket"
        
    api_url = f"{server_back_end_url}{end_point}"
    
    try:
        response = requests.put(api_url, json={'qrId':qrId})
        response.raise_for_status()
        
        if response.status_code  == 200:
            print("Porte ouverte")
        elif response.status_code  == 404:
            print("Titre de transport introuvable")
        elif response.status_code  == 410:
            print("Titre de transport périmé")
        else:
            print("Erreur coté serveur distant")

    except requests.exceptions.RequestException as e:
        error_message = f"Erreur de requête vers l'URL distante 1: {str(e)}"
        return {
            "status": 500, 
            "error": error_message
        }, 500