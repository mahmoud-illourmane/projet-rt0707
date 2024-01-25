from app import app, DATABASE_NAME, MONGO_URI          
from flask import jsonify, request
import json, base64, datetime
from pymongo.errors import PyMongoError

from src.classes.mongoDb import MongoDBManager
from src.classes.user import User
from src.classes.ticket import Ticket
from src.classes.badge import Badge

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

# Connexion à la Base de données
db_manager = MongoDBManager(MONGO_URI, DATABASE_NAME)

#
#   Authentification
#

@app.route('/api/sign-up', methods=['POST'])
def signUp():

    if request.method == 'POST':
        try:
            # Récuperation des données d'inscription
            user_data = request.get_json()
            
            new_user = User(db_manager, user_data.get('firstName'), user_data.get('email'), user_data.get('password'), 1)
            response = new_user.createUser()
            return response
        except Exception as e:
            return jsonify({
                "status": 500,
                "error": "Erreur de réception des données coté serveur."
            }), 500
        
@app.route('/api/log-in', methods=['POST'])
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
                user = User.login(db_manager, email, password)
                return user
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
    response = {
            "status": 405,
            "error": "Vous devez utiliser une requête POST pour cette route."
    }
    return jsonify(response), 405

@app.route('/api/delete-user', methods=['POST'])
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

@app.route('/api/get/generals-infos-user', methods=['GET'])
def getGeneralsInfosUser():
    if request.method == 'GET':
        user_id = request.args.get('user_id', default=None, type=str)

        result = User.getGeneralsInfosUser(db_manager, user_id)
        
        return result
    response = {
        "status": 405,
        "error": "Vous devez utiliser une requête POST pour cette route."
    }
    return jsonify(response), 405 

@app.route('/api/purchase', methods=['POST'])
def purchase():
    if request.method == 'POST':
        user_id = None
        date_achat = datetime.datetime.now()
        validite = date_achat + datetime.timedelta(days=365)
        etat = 'N'
        type_ticket = None
        
        try:
            data_receive = request.get_json()
            
            # Je vérifie si l'achat est effectué par un utilisateur authentifié
            if 'user_id' in data_receive:
                user_id = data_receive['user_id']
        except Exception as e:
            return jsonify({
                "status": 500, 
                "error": str(e)
            }), 500
        
        if data_receive['selectType'] not in ['Badge', '2H', '1J']:
            return jsonify({
                "status": 400, 
                "error": 'Sélection de type invalide.'
            }), 400
  
        type_ticket = data_receive['selectType']
        
        if type_ticket == 'Badge':
            validite = date_achat + datetime.timedelta(days=30)
            new_badge = Badge(db_manager, date_achat, validite, etat, None, user_id)
            result = new_badge.createBadge()
        else:    
            new_ticket = Ticket(db_manager, date_achat, type_ticket, validite, etat, None, user_id)
            result = new_ticket.createTicket()

        return result       
            
    response = {
            "status": 405,
            "error": "Vous devez utiliser une requête POST pour cette route."
    }
    return jsonify(response), 405