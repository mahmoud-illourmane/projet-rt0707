from app import app                             # Importation du fichier de configuration Flask
from flask import jsonify, request
import json, base64

"""
|
|   This file contains the REST API routes for the project.
|
|   Author: Mahmoud ILLOURMANE
|   Date: December 20, 2023
|
"""

"""
|   ===============
|   API REST ROUTES
|   ===============
"""

#
#   Authentification
#

@app.route('/api/signUp', methods=['POST'])
def signUp():
    """
        Endpoint pour l'enregistrement d'un nouvel utilisateur.

        Méthode HTTP supportée : POST.

        Requête JSON attendue :
        {
            "firstName": str,
            "email": str,
            "password": str
        }

        Réponses HTTP possibles :
        - 201 Created : Enregistrement réussi, renvoie les données de l'utilisateur.
        - 409 Conflict : Échec de l'enregistrement en raison d'un conflit, par exemple, un utilisateur existant avec la même adresse e-mail.
        - 400 Bad Request : Erreur de requête, avec un message explicatif.
        - 500 Internal Server Error : Erreur interne du serveur.

        :return: Une réponse JSON avec le statut HTTP approprié.
    """
    
    if request.method == 'POST':
        try:
            user_data = request.get_json()
            
            firstName = user_data.get('firstName')                      # Récupération des données
            email = user_data.get('email')
            password = user_data.get('password')
            
            try:
                new_user = User.register(email, password, firstName)    # Appel de la méthode qui enregistre un utilisateur
                
                if 'status' in new_user and new_user['status'] == 201:  # Gestion des réponses
                    return jsonify(new_user), 201
                else:
                    return jsonify(new_user), 409
            except ValueError as e:
                print(f"Une erreur est survenue : {e}")
                response = {
                    "status": 400,
                    "message": str(e)
                }
                return jsonify(response), 400
        except Exception as e:
            error_message = f"Erreur de requête vers l'URL distante : {str(e)}"
            return jsonify({
                "status": 500,
                "error": error_message
            }), 500

@app.route('/api/logIn', methods=['POST'])
def logIn():
    """
        Endpoint pour l'authentification d'un utilisateur.

        Méthode HTTP supportée : POST.

        Requête JSON attendue :
        {
            "email": str,
            "password": str
        }

        Réponses HTTP possibles :
        - 200 OK : Authentification réussie, renvoie les données de l'utilisateur.
        - 401 Unauthorized : Échec de l'authentification.
        - 400 Bad Request : Erreur de requête, avec un message explicatif.
        - 500 Internal Server Error : Erreur interne du serveur.

        :return: Une réponse JSON avec le statut HTTP approprié.
    """
    
    if request.method == 'POST':
        try:
            user_data = request.get_json()
            
            email = user_data.get('email')
            password = user_data.get('password')
            
            try:
                new_user = User.authenticate_user(email, password)
                
                if 'status' in new_user and new_user['status'] == 200:
                    return jsonify(new_user), 200
                else:
                    return jsonify(new_user), 401
            except ValueError as e:
                print(f"Une erreur est survenue : {e}")
                response = {
                    "status": 400,
                    "message": str(e)
                }
                return jsonify(response), 400
        except Exception as e:
            error_message = f"Erreur de requête vers l'URL distante : {str(e)}"
            return jsonify({
                "status": 500,
                "error": error_message
            }), 500

@app.route('/api/deleteUser', methods=['POST'])
def deleteUser():
    """
        Endpoint pour supprimer un utilisateur.

        Méthode HTTP supportée : POST.

        Requête JSON attendue :
        {
            "user_id": int
        }

        Réponses HTTP possibles :
        - 204 No Content : Utilisateur supprimé avec succès.
        - 409 No Content : Utilisateur n'a pas été supprimé.
        - 400 Bad Request : Erreur de requête, avec un message explicatif.
        - 500 Internal Server Error : Erreur interne du serveur.

        :return: Une réponse JSON avec le statut HTTP approprié.
    """
    
    if request.method == 'POST':
        try:
            user_data = request.get_json()
            user_id = user_data.get('user_id')                                  # Reception de l'id de l'utilisateur

            try:
                bool = User.delete_user(user_id)                                # Appel de la méthode de classe pour supprimer un utilisateur
                if bool:
                    return jsonify({"status": 204}), 204                        # Je renvoi la bonne réponse http
                return jsonify({"status": 409}), 409
            except ValueError as e:                                             # Le reste du code est la gestion des exceptions
                print(f"Une erreur est survenue : {e}")
                response = {
                    "status": 400,
                    "message": str(e)
                }
                return jsonify(response), 400
        except Exception as e:
            error_message = f"Erreur de requête vers l'URL distante : {str(e)}"
            return jsonify({
                "status": 500,
                "error": error_message
            }), 500

#
#   Web Application
#
