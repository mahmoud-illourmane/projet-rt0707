from app import app
from flask import request, jsonify
import requests, base64
from typing import Dict, Any

from flask_login import current_user

"""
|
|   This file contains all API routes that can be called to interact with the server.
|
|   Author: Mahmoud ILLOURMANE
|   Date: January 18, 2024
|
"""

# Accède à la variable globale depuis la configuration Flask
server_back_end_url = app.config['SERVER_BACK_END_URL']

#
#
#   Authentification
#
#

# if current_user.is_authenticated:
#     user_id = current_user.id
            
@app.route('/api/signUp', methods=['POST'])
def handleSignUp():
    """_summary_
    Cette méthode se charge d'envoyer les données d'inscription au serveur backend.
    
    Returns:
        _type_: une réponse Json
    """
    
    if request.method == 'POST':                                                # Je vérifi que la requête a bien été faite avec POST
        try:
            user_data = request.get_json()                                      # Récupération des données JSON reçus
            data_register = {                                                   # Je forge les données à envoyer
                "firstName": user_data.get('firstName'),
                "email": user_data.get('email'),
                "password": user_data.get('password')
            }
        except Exception as e:                                                  # Gestion de l'exception
            error_message = f"Erreur de requête vers l'URL distante : {str(e)}"
            return jsonify({                                                    # Je retourne un message d'erreur
                "status": 500,
                "error": error_message
            }), 500
        
        try:
            api_url = f"{server_back_end_url}/api/signUp"                       # Préparation de l'url du serveur distant
            response = requests.post(api_url, json=data_register)               # Envoi des données au serveur sitant en utilisant une requête POST
            
                                                                                # Gestion de la réponse du serveur Backend 
            if response.status_code == 201:                                     # 201 indique que l'inscription s'est bien déroulé                          
                response_data = response.json()
                id = response_data.get('id')
                first_name = response_data.get('first_name')
                email = response_data.get('email')
                print('id: ', id, ' first name:', first_name)
                return jsonify({
                    "status": 201,
                    "id" : id,
                    "email" : email,
                    "first_name" : first_name,
                }), 201
                # return jsonify(response), 201
            elif response.status_code == 500:
                return jsonify({
                    "status": 500,
                    "error" : "error serveur frontend"
                }), 500
            else:
                return jsonify({
                    "status": 409,
                    "error" : "L'email est déjà utilisé."
                }), 409
        except requests.exceptions.RequestException as e:
            print(f"Erreur de requête vers l'API du back-end : {e}")
            
            return jsonify({
                "status": 500, 
                "message": "Erreur de communication avec l'API du back-end"
            }), 500
            
    response = {
            "status": 405,
            "error": "Vous devez utiliser une requête POST pour cette route."
    }
    return jsonify(response), 405
    
@app.route('/api/logIn', methods=['POST'])
def handleLogIn():
    """_summary_
    Cette méthode se charge d'authentifier un utilisateur
    
    Returns:
        _type_: une réponse Json
    """
    
    if request.method == 'POST':                                                # Je vérifi que la requête a bien été faite avec POST
        try:
            user_data = request.get_json()                                      # Récupération des données JSON reçus
            data_register = {                                                   # Je forge les données à envoyer
                "email": user_data.get('email'),
                "password": user_data.get('password')
            }
        except Exception as e:                                                  # Gestion de l'exception
            error_message = f"Erreur de requête vers l'URL distante : {str(e)}"
            return jsonify({                                                    # Je retourne un message d'erreur
                "status": 500,
                "error": error_message
            }), 500
        
        try:
            api_url = f"{server_back_end_url}/api/logIn"                        # Préparation de l'url du serveur distant
            response = requests.post(api_url, json=data_register)               # Envoi des données au serveur sitant en utilisant une requête POST
            
                                                                                # Gestion de la réponse du serveur Backend 
            if response.status_code == 200:                                     # 200 indique que l'inscription s'est bien déroulé                          
                response_data = response.json()
                id = response_data.get('id')
                first_name = response_data.get('first_name')
                email = response_data.get('email')
                return jsonify({
                    "status": 200,
                    "id" : id,
                    "email" : email,
                    "first_name" : first_name,
                }), 200
            elif response.status_code == 500:
                return jsonify({
                    "status": 500,
                    "error" : "error serveur frontend"
                }), 500
            else:
                return jsonify({
                    "status": 401,
                    "error" : "L'email ou le mot de passe est incorrect."
                }), 401
        except requests.exceptions.RequestException as e:
            print(f"Erreur de requête vers l'API du back-end : {e}")
            
            return jsonify({
                "status": 500, 
                "message": "Erreur de communication avec l'API du back-end"
            }), 500
            
    response = {
            "status": 405,
            "error": "Vous devez utiliser une requête POST pour cette route."
    }
    return jsonify(response), 405

@app.route('/api/deleteUser', methods=['POST'])
def deleteUser():
    """_summary_
    Cette méthode se charge de supprimer un utilisateur
    
    Returns:
        _type_: une réponse Json
    """
    
    if request.method == 'POST':                                                # Je vérifi que la requête a bien été faite avec POST
        
        try:
            user_data = request.get_json()                                      # Récupération des données JSON reçus
            user_id = user_data.get('user_id')
            
        except Exception as e:                                                  # Gestion de l'exception
            error_message = f"Erreur de requête vers l'URL distante : {str(e)}"
            return jsonify({                                                    # Je retourne un message d'erreur
                "status": 500,
                "error": error_message
            }), 500
            
        try:
            api_url = f"{server_back_end_url}/api/deleteUser"                   # Préparation de l'url du serveur distant
            response = requests.post(api_url, json={"user_id": user_id})               
                                                                                # Gestion de la réponse du serveur Backend 
            if response.status_code == 204:                                     # 204 indique que l'inscription s'est bien déroulé         
                response = request.get_json()                  
                return jsonify({
                    "status": 204, 
                }), 204
            else:
                return jsonify({
                    "status": 400, 
                }), 400
        except requests.exceptions.RequestException as e:
            print(f"Erreur de requête vers l'API du back-end : {e}")
            
            return jsonify({
                "status": 500, 
                "message": "Erreur de communication avec l'API du back-end"
            }), 500
            
    response = {
            "status": 405,
            "error": "Vous devez utiliser une requête POST pour cette route."
    }
    return jsonify(response), 405

#
#
#   Web Application
#
#
