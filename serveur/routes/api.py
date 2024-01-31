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
    """
        Inscription d'un nouvel utilisateur.

        Cette route permet à un nouvel utilisateur de s'inscrire en utilisant une requête POST. Les données d'inscription
        doivent être fournies dans le corps de la requête au format JSON.

        Args:
            - firstName (str, obligatoire): Le prénom de l'utilisateur.
            - email (str, obligatoire): L'adresse e-mail de l'utilisateur.
            - password (str, obligatoire): Le mot de passe de l'utilisateur.

        Returns:
            - Statut 200 avec un message de confirmation si l'inscription a réussi.
            - Statut 500 en cas d'erreur lors de la réception des données.

        Exemple d'utilisation:
            Pour s'inscrire avec les données suivantes :
            {
                "firstName": "Toto",
                "email": "toto@example.com",
                "password": "password"
            }
            Effectuez une requête POST avec ces données au format JSON.
    """

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
        Supprimer un utilisateur.

        Cette route permet de supprimer un utilisateur en utilisant une requête POST. L'identifiant de l'utilisateur
        doit être fourni dans le corps de la requête au format JSON.

        Args:
            - user_id (str, obligatoire): L'identifiant de l'utilisateur à supprimer.

        Returns:
            - Statut 204 si l'utilisateur a été supprimé avec succès.
            - Statut 409 si une erreur s'est produite lors de la suppression.

        Raises:
            - Une exception est levée si l'identifiant de l'utilisateur n'est pas fourni ou s'il n'existe pas.

        Exemple d'utilisation:
            Pour supprimer l'utilisateur avec l'identifiant '12345', effectuez une requête POST avec le corps JSON :
            {
                "user_id": "12345"
            }
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

@app.route('/api/get/tickets-user', methods=['GET'])
def getAllTicketsUser():
    """
        Récupérer tous les tickets d'un utilisateur.

        Cette route permet de récupérer tous les tickets d'un utilisateur en utilisant une requête GET. L'identifiant
        de l'utilisateur est inclus en tant que paramètre de requête.

        Args:
            - user_id (str, obligatoire): L'identifiant de l'utilisateur dont on souhaite obtenir les tickets.

        Returns:
            - Les tickets de l'utilisateur spécifié.

        Raises:
            - Une exception est levée si l'identifiant de l'utilisateur n'est pas fourni ou s'il n'existe pas.

        Exemple d'utilisation:
            Pour obtenir tous les tickets de l'utilisateur avec l'identifiant '12345', effectuez une requête GET avec
            le paramètre 'user_id=12345'.
    """
    
    if request.method == 'GET':
        user_id = request.args.get('user_id', default=None, type=str)

        if user_id == None:
            response = {
                "status": 403,
                "error": "Aucun ID fournis."
            }
            return jsonify(response), 200 
        Ticket.verifierTicketsPerimes(db_manager)
        result = User.getAllTicketsUser(db_manager, user_id)

        return result
    response = {
        "status": 405,
        "error": "Vous devez utiliser une requête GET pour cette route."
    }
    return jsonify(response), 200

@app.route('/api/get/generals-infos-user', methods=['GET'])
def getGeneralsInfosUser():
    """
        Récupérer les informations générales d'un utilisateur.

        Cette route permet de récupérer les informations générales d'un utilisateur en utilisant une requête GET. L'identifiant
        de l'utilisateur est inclus en tant que paramètre de requête.

        Args:
            - user_id (str, facultatif): L'identifiant de l'utilisateur dont on souhaite obtenir les informations.

        Returns:
            - Les informations générales de l'utilisateur spécifié.

        Raises:
            - Une exception est levée si l'identifiant de l'utilisateur n'est pas valide ou si l'utilisateur n'existe pas.

        Exemple d'utilisation:
            Pour obtenir les informations générales de l'utilisateur avec l'identifiant '12345', effectuez une requête GET avec
            le paramètre 'user_id=12345'.
    """

    if request.method == 'GET':
        user_id = request.args.get('user_id', default=None, type=str)

        result = User.getGeneralsInfosUser(db_manager, user_id)
        
        return result
    response = {
        "status": 405,
        "error": "Vous devez utiliser une requête POST pour cette route."
    }
    return jsonify(response), 200

@app.route('/api/purchase', methods=['POST'])
def purchase():
    """
        Effectuer un achat de ticket ou de badge.

        Cette route permet à un utilisateur d'effectuer un achat de ticket ou de badge en utilisant une requête POST. Les
        informations de l'achat, telles que le type de ticket ou de badge, la date d'achat, la validité, etc., sont incluses
        dans le corps de la requête JSON.

        Args:
            - selectType (str): Le type de ticket ou de badge à acheter (peut être 'Badge', '2H' ou '1J').
            - user_id (str, optional): L'identifiant de l'utilisateur effectuant l'achat. Facultatif si l'utilisateur est
            authentifié.

        Returns:
            - Les résultats de l'opération d'achat du ticket ou du badge.

        Raises:
            - Une exception est levée si les données de la requête sont incorrectes ou si le type de ticket/badge est invalide.

        Exemple d'utilisation:
            Pour effectuer un achat de badge, effectuez une requête POST avec les informations nécessaires dans le corps de la
            requête JSON.
    """

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
            new_badge = Badge(db_manager, date_achat, validite, etat, 0, None, user_id)
            result = new_badge.createBadge()
        else:    
            new_ticket = Ticket(db_manager, date_achat, type_ticket, validite, etat, 0, None, user_id)
            result = new_ticket.createTicket()

        return result       
            
    response = {
            "status": 405,
            "error": "Vous devez utiliser une requête POST pour cette route."
    }
    return jsonify(response), 405

#
# Simulation porte
#

@app.route('/api/scanne/ticket', methods=['PUT'])
def scanneTicket():
    """
        Scanner un ticket.

        Cette route permet de scanner un ticket en utilisant une requête PUT. Elle prend en compte le ticket_id et effectue
        les opérations nécessaires pour scanner le ticket.

        Args:
            ticket_id (dict): Un dictionnaire contenant les informations du ticket à scanner.

        Returns:
            - Les résultats de l'opération de scan du ticket.

        Raises:
            Aucune exception n'est levée dans cette fonction.

        Exemple d'utilisation:
            Pour scanner un ticket, effectuez une requête PUT avec les informations du ticket à scanner.
    """
    
    if request.method == 'PUT':
        data = request.get_json()
        print('SCAN TICKET : données reçus.', data)
        
        ticket_id = data['qrId']
        result = Ticket.scannerTicket(ticket_id, db_manager)
        return result
    response = {
        "status": 405,
        "error": "Vous devez utiliser une requête PUT pour cette route."
    }
    return jsonify(response), 405

@app.route('/api/scanne/badge', methods=['PUT'])
def scanneBadge():
    """
        Scanner un badge.

        Cette route permet de scanner un badge en utilisant une requête PUT. Elle prend en compte le badge_id et effectue
        les opérations nécessaires pour scanner le badge.

        Args:
            badge_id (dict): Un dictionnaire contenant les informations du badge à scanner.

        Returns:
            - Les résultats de l'opération de scan du badge.

        Raises:
            Aucune exception n'est levée dans cette fonction.

        Exemple d'utilisation:
            Pour scanner un badge, effectuez une requête PUT avec les informations du badge à scanner.
    """
    
    if request.method == 'PUT':
        data = request.get_json()
        print('SCAN BADGE : ', data)
        
        badge_id = data['qrId']
        result = Badge.scannerBadge(badge_id, db_manager)
        
        return result
    response = {
        "status": 405,
        "error": "Vous devez utiliser une requête PUT pour cette route."
    }
    return jsonify(response), 405

#
#   Settings
#

@app.route('/api/settings', methods=['PUT'])
def updateDataSettings():
    """
        Met à jour les paramètres de l'utilisateur.

        Cette route permet à un utilisateur de mettre à jour ses paramètres, y compris le prénom, l'email et le mot de passe.

        Args:
            data (dict): Un dictionnaire contenant les données de mise à jour, y compris l'opération à effectuer,
                        l'ID de l'utilisateur et les nouvelles données (selon l'opération).

        Returns:
            - Un résultat indiquant le succès ou l'échec de la mise à jour.

        Raises:
            Aucune exception n'est levée dans cette fonction.

        Exemple d'utilisation:
            Pour mettre à jour les paramètres de l'utilisateur, une requête PUT doit être effectuée vers cette route avec les données de mise à jour appropriées.
    """
    
    if request.method == 'PUT':
        data = request.get_json()
        
        print(data)
        
        operation = int(data['operation_id'])
        user_id = str(data['user_id'])
        
        if operation not in [1, 2, 3]:
            response = {
                "status": 400,
                "error": "Opération ID inconnue."
            }
            return jsonify(response), 200
        
        if operation == 1:
            new_data = str(data['data'])
            result = User.updateFirstName(db_manager, user_id, new_data)
        elif operation == 2:
            new_data = str(data['data'])
            result = User.updateEmail(db_manager, user_id, new_data)
        elif operation == 3:
            old_password = str(data['oldPassword'])
            new_password = str(data['newPassword'])
            confirm_new_password = str(data['confirmPassword'])
            result = User.updatePassword(db_manager, user_id, old_password, new_password, confirm_new_password)
        
        return result
    response = {
        "status": 405,
        "error": "Vous devez utiliser une requête POST pour cette route."
    }
    return jsonify(response), 200

@app.route('/api/delete/account', methods=['POST'])
def deleteAccount():
    """
        Supprime un compte utilisateur.

        Cette route permet de supprimer un compte utilisateur à partir de l'ID utilisateur fourni dans la requête POST.
        La suppression d'un compte utilisateur est une opération sensible qui nécessite une authentification appropriée.

        Args:
            user_id (str): L'ID de l'utilisateur à supprimer.

        Returns:
            - Un résultat indiquant le succès ou l'échec de la suppression.

        Raises:
            Aucune exception n'est levée dans cette fonction.

        Exemple d'utilisation:
            Pour supprimer un compte utilisateur, une requête POST doit être effectuée vers cette route avec l'ID de l'utilisateur à supprimer.
    """
    
    if request.method == 'POST':  
        user_data = request.get_json()
        user_id = user_data.get('user_id')
            
        result = User.deleteUser(db_manager, user_id)
            
        return result
    response = {
        "status": 405,
        "error": "Vous devez utiliser une requête POST pour cette route."
    }
    return jsonify(response), 405

#
#   Admin Pannel
#

@app.route('/api/admin/get/all-users', methods=['GET'])
def getAdminAllUsers():
    """
        Récupère toutes les informations des utilisateurs avec le rôle 1 pour le panneau d'administration.

        Cette route permet à un administrateur d'obtenir des informations détaillées sur tous les utilisateurs ayant le rôle 1.

        Returns:
            - Une liste des utilisateurs avec des informations agrégées sur les tickets et les badges.

        Raises:
            Aucune exception n'est levée dans cette fonction.
    """
    
    if request.method == 'GET':
        
        result = User.getAdminAllUsers(db_manager)
        return result
    response = {
        "status": 405,
        "error": "Vous devez utiliser une requête GET pour cette route."
    }
    return jsonify(response), 200 
