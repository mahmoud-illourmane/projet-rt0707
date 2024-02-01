from app import app
from flask import request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, login_required, current_user

import requests
from functools import wraps

from src.classes.user import User
from src.classes.tools import write_log

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
server_door_url = app.config['SERVER_DOOR_URL']

#
#   Authentification
#

# if current_user.is_authenticated:
#     user_id = current_user.id
            
# Initialisation de LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Définissez une liste de rôles autorisés
# 1 : User, 2 : Admin, 3 : Emp
AUTHORIZED_ROLES = [1, 2, 3] 

def roles_required(allowed_roles):
    """
        Cette fonction est un décorateur personnalisé pour gérer les rôles requis pour accéder à une route dans Flask.
        
        Args:
            allowed_roles (list): Une liste des rôles autorisés pour accéder à la route.

        Returns:
            function: Un décorateur qui vérifie si l'utilisateur actuellement authentifié a le rôle requis.
                    Si l'utilisateur a le bon rôle, la vue associée est exécutée normalement.
                    Sinon, une erreur 403 (Forbidden) est renvoyée.
    """
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated and current_user.role in allowed_roles:
                return func(*args, **kwargs)
            else:
                return redirect(url_for('custom_403_error_page'))
        return wrapper
    return decorator

@login_manager.user_loader
def load_user(user_id):
    """
        Charge un objet utilisateur en fonction de l'identifiant fourni.

        Cette fonction est appelée par Flask-Login pour récupérer un objet utilisateur en fonction de l'identifiant de l'utilisateur (user_id).

        Paramètres :
            user_id (str) : L'identifiant de l'utilisateur à charger.

        Retourne :
            Objet User ou None : Une instance de la classe User représentant l'utilisateur chargé, ou None si l'utilisateur n'est pas trouvé.
    """
    
    # Récupère les informations de l'utilisateur depuis la session Flask
    user_session = session.get('user_session')
    
    # Vérifie si l'utilisateur est authentifié et si l'identifiant fourni correspond à l'identifiant stocké
    if user_session and user_id == user_session.get('id'):
        # Crée et retourne un objet User avec les informations de la session
        return User(user_id, user_session.get('first_name'), user_session.get('email'), user_session.get('role'))
    
    # Si l'utilisateur n'est pas trouvé ou si l'identifiant ne correspond pas, retourne None
    return None

@app.route('/api/sign-up', methods=['POST'])
def handleSignUp():
    """
        Cette méthode se charge d'envoyer les données d'inscription au serveur backend.
        
        Returns:
            _type_: une réponse Json
    """
    
    if request.method == 'POST':
        # Récupération des données du formulaire
        first_name = request.form.get('firstName')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('passwordConfirm')
        
        if password != password_confirm:
            flash('Vos mots de passe ne correspondent pas.', 'error') 
            return redirect(url_for('signUp', 
                first_name=first_name, 
                email=email, 
                password=password,
                passwordConfirm=password_confirm))
        
        data = {
            'firstName': first_name,
            'email': email,
            'password': password,
            'passwordConfirm': password_confirm
        }
    
        try:
            # Spécification de l'en-tête 'Content-Type' pour indiquer que nous envoyons du JSON
            headers = {'Content-Type': 'application/json'}
            api_url = f"{server_back_end_url}/api/sign-up"
            response = requests.post(api_url, json=data, headers=headers)
            
            # Vous pouvez gérer la réponse du serveur backend comme nécessaire
            if response.status_code == 201:
                new_user_data = response.json()
                
                user_id = new_user_data.get('id')
                role = int(new_user_data.get('role'))
                
                if user_id is not None:
                    user = User(user_id, first_name, email, role)
                    login_user(user)

                    session['user_session'] = {
                        'id': user.get_id(),
                        'first_name': user.get_fisrt_name(),
                        'email': user.get_email(),
                        'role': user.get_role()
                    }
                    
                    flash('Inscription réussie', 'success')  
                    return redirect(url_for('index'))
                else:
                    flash('Données d\'utilisateur manquantes dans la réponse', 'error')  
                    return redirect(url_for('signUp'))
                
            elif response.status_code == 304:
                flash('l\'adresse e-mail que vous avez saisie est déjà utilisée.', 'error')  
                return redirect(url_for('signUp'))
            elif response.status_code == 400:
                flash(response.json().get('error', 'Erreur inconnue'), 'error')  
                return redirect(url_for('signUp'))
            elif response.status_code == 500:
                flash(response.json().get('error', 'Erreur inconnue'), 'error')  
                return redirect(url_for('signUp'))
            else:
                flash('Erreur lors de l\'inscription', 'error') 
                return redirect(url_for('signUp', first_name=first_name))
        
        except Exception as e:
            flash(f"Erreur lors de l'envoi de la requête POST : {str(e)}", 'error') 
            return redirect(url_for('signUp'))
   
    flash('Vous devez utiliser une requête POST', 'error')  
    return redirect(url_for('signUp'))
    
@app.route('/api/log-in', methods=['POST'])
def handleLogIn():
    """
        Cette méthode se charge d'authentifier un utilisateur
        
        Returns:
            _type_: une réponse Json
    """
    
    if request.method == 'POST':                                                # Je vérifi que la requête a bien été faite avec POST
        email = request.form.get('email')
        password = request.form.get('password')
        
        data = {
            'email': email,
            'password': password,
        }
        
        try:
            # Spécification de l'en-tête 'Content-Type' pour indiquer que nous envoyons du JSON
            headers = {'Content-Type': 'application/json'}
            api_url = f"{server_back_end_url}/api/log-in"                       # Préparation de l'url du serveur distant
            response = requests.post(api_url, json=data, headers=headers)
                                                                                # Gestion de la réponse du serveur Backend 
            if response.status_code == 200:                                     # 200 indique que l'inscription s'est bien déroulé                          
                user_data = response.json()

                if user_data.get('id') is not None:
                    user = User(str(user_data.get('id')), user_data.get('first_name'), user_data.get('email'), int(user_data.get('role')))
                    login_user(user)

                    session['user_session'] = {
                        'id': user.get_id(),
                        'first_name': user.get_fisrt_name(),
                        'email': user.get_email(),
                        'role': user.get_role()
                    }
                    
                    # Redirection de l'utilisateur vers la vue appropriée
                    flash('Bienvenue', 'success')  
                    if int(current_user.role) == 1:
                        return redirect(url_for('index'))
                    elif int(current_user.role) == 2:
                        return redirect(url_for('admin_dashboard'))
                else:
                    flash('Une erreur s\'est produite.', 'error')  
                    return redirect(url_for('login'))
            elif response.status_code == 401:
                flash("Email ou mot de passe incorrect", 'error') 
                return redirect(url_for('login'))
                
            elif response.status_code == 500:
                flash("Error serveur distant", 'error') 
                return redirect(url_for('login'))

        except requests.exceptions.RequestException as e:
            flash(f"Erreur de requête vers l'API du back-end : {e}", 'error') 
            return redirect(url_for('login'))
            
    response = {
            "status": 405,
            "error": "Vous devez utiliser une requête POST pour cette route."
    }
    return jsonify(response), 405

@app.route('/api/deleteUser', methods=['POST'])
def deleteUser():
    """
        Supprime un utilisateur en utilisant une requête POST.

        Cette route permet de supprimer un utilisateur en envoyant une requête POST
        contenant un objet JSON avec la clé "user_id" pour identifier l'utilisateur à supprimer.

        Args:
            Aucun argument n'est requis dans la fonction.

        Returns:
            - Si la suppression réussit, la fonction retourne un code de statut 204 (No Content).
            - Si la suppression échoue, la fonction retourne un code de statut 400 (Bad Request).
            - Si une erreur inattendue se produit lors de la communication avec le serveur Backend,
            la fonction retourne un code de statut 500 (Internal Server Error) avec un message d'erreur.

        Raises:
            Aucune exception n'est levée dans cette fonction.

        Exemple d'utilisation:
            Pour supprimer un utilisateur, envoyez une requête POST à cette route avec un objet JSON
            contenant la clé "user_id" spécifiant l'identifiant de l'utilisateur à supprimer.
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

@app.route('/api/get/generals-infos-user', methods=['GET'])
@login_required
def getGeneralsInfosUser():
    """
        Récupère les informations générales de l'utilisateur en utilisant une requête GET.

        Cette route permet de récupérer les informations générales de l'utilisateur actuellement authentifié.
        Elle nécessite une authentification préalable, ce qui signifie que l'utilisateur doit être connecté.

        Args:
            Aucun argument n'est requis dans la fonction.

        Returns:
            - Si l'utilisateur est authentifié, la fonction retourne les informations générales de l'utilisateur au format JSON.
            - Si l'utilisateur n'est pas authentifié, la fonction retourne un code de statut 405 (Method Not Allowed)
            avec un message d'erreur indiquant que seule une requête GET est autorisée.

        Raises:
            Aucune exception n'est levée dans cette fonction.

        Exemple d'utilisation:
            Pour récupérer les informations générales de l'utilisateur actuellement authentifié, envoyez une requête GET à cette route.
    """
    
    if request.method == 'GET':  
        
        # Si l'utilisateur est authentifier on envoi son id
        if current_user.is_authenticated:
            user_id = str(current_user.id)
            
        api_url = f"{server_back_end_url}/api/get/generals-infos-user"
        
        try:
            response = requests.get(api_url, params={'user_id': user_id})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Erreur de requête vers l'URL distante 1: {str(e)}"
            return jsonify({
                "status": 500, 
                "error": error_message
            }), 500
    response = {
            "status": 405,
            "error": "Vous devez utiliser une requête GET pour cette route."
    }

@app.route('/api/get/tickets-user', methods=['GET'])
@login_required
def getAllTicketsUser():
    """
        Récupère tous les tickets de l'utilisateur en utilisant une requête GET.

        Cette route permet de récupérer tous les tickets de l'utilisateur actuellement authentifié.
        Elle nécessite une authentification préalable, ce qui signifie que l'utilisateur doit être connecté.

        Args:
            Aucun argument n'est requis dans la fonction.

        Returns:
            - Si l'utilisateur est authentifié, la fonction retourne la liste de tous les tickets de l'utilisateur au format JSON.
            - Si l'utilisateur n'est pas authentifié, la fonction retourne un code de statut 403 (Forbidden)
            avec un message d'erreur indiquant que l'authentification est requise.
            - Si une erreur se produit lors de la requête vers le serveur distant, la fonction retourne un code de statut 500 (Internal Server Error)
            avec un message d'erreur approprié.

        Raises:
            Aucune exception n'est levée dans cette fonction.

        Exemple d'utilisation:
            Pour récupérer tous les tickets de l'utilisateur actuellement authentifié, envoyez une requête GET à cette route.
    """
    
    if request.method == 'GET':
        # Si l'utilisateur est authentifier on envoi son id
        if current_user.is_authenticated:
            user_id = str(current_user.id)
        else:
            response = {
                "status": 403,
                "error": "Vous devez être authentifié."
            }
            return jsonify(response), 200 
    
        api_url = f"{server_back_end_url}/api/get/tickets-user"
        
        try:
            response = requests.get(api_url, params={'user_id': user_id})
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Erreur de requête vers l'URL distante 1: {str(e)}"
            return jsonify({
                "status": 500, 
                "error": error_message
            }), 500
    response = {
        "status": 405,
        "error": "Vous devez utiliser une requête GET pour cette route."
    }
    return jsonify(response), 405 

@app.route('/api/purchase', methods=['POST'])
def purchase():
    """
        Effectue un achat en utilisant une requête POST.

        Cette route permet à un utilisateur d'effectuer un achat en envoyant une requête POST avec les données d'achat au serveur distant.
        Si l'utilisateur est authentifié, son identifiant est ajouté aux données d'achat.

        Args:
            Aucun argument n'est requis dans la fonction.

        Returns:
            - Si la requête POST réussit, la fonction retourne la réponse du serveur distant au format JSON.
            - Si une erreur se produit lors de la requête vers le serveur distant, la fonction retourne un code de statut 500 (Internal Server Error)
            avec un message d'erreur approprié.

        Raises:
            Aucune exception n'est levée dans cette fonction.

        Exemple d'utilisation:
            Pour effectuer un achat, envoyez une requête POST à cette route avec les données d'achat au format JSON.
            Si l'utilisateur est authentifié, assurez-vous d'inclure son identifiant dans les données.
    """
    
    if request.method == 'POST':  
        data = request.get_json()
        
        # Si l'utilisateur est authentifier on envoi son id
        if current_user.is_authenticated:
            data['user_id'] = str(current_user.id)

        api_url = f"{server_back_end_url}/api/purchase"
        
        try:
            response = requests.post(api_url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Erreur de requête vers l'URL distante 2: {str(e)}"
            return jsonify({
                "status": 500, 
                "error": error_message
            }), 500
    response = {
            "status": 405,
            "error": "Vous devez utiliser une requête POST pour cette route."
    }

#
#
#   Settings Pannel
#
#

@app.route('/api/settings', methods=['PUT'])
@login_required
def updateDataSettings():
    """
        Met à jour les paramètres utilisateur en utilisant une requête PUT.

        Cette route permet à un utilisateur authentifié de mettre à jour ses paramètres en envoyant une requête PUT avec les données de mise à jour
        au serveur distant. L'identifiant de l'utilisateur est ajouté aux données de mise à jour s'il est authentifié.

        Args:
            Aucun argument n'est requis dans la fonction.

        Returns:
            - Si la requête PUT réussit, la fonction retourne la réponse du serveur distant au format JSON.
            - Si l'utilisateur n'est pas authentifié, la fonction retourne un code de statut 500 (Internal Server Error) avec un message d'erreur.
            - Si une erreur se produit lors de la requête vers le serveur distant, la fonction retourne un code de statut 500 (Internal Server Error)
            avec un message d'erreur approprié.

        Raises:
            Aucune exception n'est levée dans cette fonction.

        Exemple d'utilisation:
            Pour mettre à jour les paramètres, envoyez une requête PUT à cette route avec les données de mise à jour au format JSON.
            Assurez-vous d'inclure l'identifiant de l'utilisateur dans les données si l'utilisateur est authentifié.
    """

    if request.method == 'PUT':
        data = request.get_json()
        
        # Si l'utilisateur est authentifier j'ajoute son id
        if current_user.is_authenticated:
            data['user_id'] = str(current_user.id)
        else:
            return jsonify({
                "status": 500, 
                "error": "Aucun ID trouvé pour l'utilisateur."
            }), 500

        api_url = f"{server_back_end_url}/api/settings"
        try:
            response = requests.put(api_url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Erreur de requête vers l'URL distante 1: {str(e)}"
            return jsonify({
                "status": 500, 
                "error": error_message
            }), 500
    response = {
        "status": 405,
        "error": "Vous devez utiliser une requête PUT pour cette route."
    }
    return jsonify(response), 405 

@app.route('/api/delete/account', methods=['POST'])
@login_required
def deleteAccount():
    """
        Supprime le compte utilisateur en utilisant une requête POST.

        Cette route permet à un utilisateur authentifié de supprimer son compte en envoyant une requête POST au serveur distant avec son identifiant.
        Après la suppression du compte, la session de l'utilisateur est également effacée.

        Args:
            Aucun argument n'est requis dans la fonction.

        Returns:
            - Si la requête POST réussit et retourne un code de statut 200, la fonction efface la session de l'utilisateur, affiche un message de
            confirmation et redirige l'utilisateur vers la page d'inscription.
            - Si l'utilisateur n'est pas authentifié, la fonction affiche un message d'erreur et redirige l'utilisateur vers la page des paramètres.
            - Si une erreur se produit lors de la requête vers le serveur distant, la fonction affiche un message d'erreur approprié et redirige
            l'utilisateur vers la page des paramètres.

        Raises:
            Aucune exception n'est levée dans cette fonction.

        Exemple d'utilisation:
            Pour supprimer un compte, envoyez une requête POST à cette route avec l'identifiant de l'utilisateur dans les données JSON.
            Si la suppression réussit, l'utilisateur sera redirigé vers la page d'inscription avec un message de confirmation.
    """
    
    if request.method == 'POST':
        if current_user.is_authenticated:
            user_id = current_user.id
        else:
            flash('Une erreur pendant la récupération de votre ID.', 'error')  
            return redirect(url_for('settings'))
        
        api_url = f"{server_back_end_url}/api/delete/account"
        try:
            response = requests.post(api_url, json={'user_id': user_id})
            response.raise_for_status()
            if(response.status_code  == 200):
                session.clear()
                flash('Votre compte à bien été supprimé', 'error')  
                return redirect(url_for('signUp'))
            
            flash('Une erreur s\'est produite pendant la suppression.', 'error')  
            return redirect(url_for('settings'))
        except requests.exceptions.RequestException as e:
            flash(f"Erreur de requête vers l'URL distante 1: {str(e)}", 'error')  
            return redirect(url_for('settings'))
            
    flash('Vous devez utiliser une requête POST', 'error')  
    return redirect(url_for('settings'))


#
#
#   Iot Simulation
#
#

@app.route('/api/scanne/ticket', methods=['PUT'])
def scanneTicket():
    """
        Marque un ticket comme scanné en utilisant une requête PUT.

        Cette route permet de marquer un ticket spécifié comme scanné en utilisant une requête PUT.
        Elle nécessite l'envoi d'un JSON contenant l'identifiant du ticket à marquer comme scanné.

        Args:
            Aucun argument n'est requis dans la fonction.

        Returns:
            - Si la requête PUT réussit, la fonction retourne la réponse du serveur distant au format JSON.
            - Si une erreur se produit lors de la requête vers le serveur distant, la fonction retourne un code de statut 500 (Internal Server Error)
            avec un message d'erreur approprié.

        Raises:
            Aucune exception n'est levée dans cette fonction.

        Exemple d'utilisation:
            Pour marquer un ticket comme scanné, envoyez une requête PUT à cette route avec un JSON contenant l'identifiant du ticket.
    """
    
    if request.method == 'PUT':
        ticket = request.get_json()
        ticket_id = ticket.get('ticket_id')
        
        api_url = f"{server_back_end_url}/api/scanne/ticket"
        try:
            response = requests.put(api_url, json=ticket_id)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Erreur de requête vers l'URL distante 1: {str(e)}"
            return jsonify({
                "status": 500, 
                "error": error_message
            }), 500
    response = {
        "status": 405,
        "error": "Vous devez utiliser une requête PUT pour cette route."
    }
    return jsonify(response), 405 

@app.route('/api/scanne/badge', methods=['PUT'])
def scanneBadge():
    """
        Marque un badge comme scanné en utilisant une requête PUT.

        Cette route permet de marquer un badge spécifié comme scanné en utilisant une requête PUT.
        Elle nécessite l'envoi d'un JSON contenant l'identifiant du badge à marquer comme scanné.

        Args:
            Aucun argument n'est requis dans la fonction.

        Returns:
            - Si la requête PUT réussit, la fonction retourne la réponse du serveur distant au format JSON.
            - Si une erreur se produit lors de la requête vers le serveur distant, la fonction retourne un code de statut 500 (Internal Server Error)
            avec un message d'erreur approprié.

        Raises:
            Aucune exception n'est levée dans cette fonction.

        Exemple d'utilisation:
            Pour marquer un badge comme scanné, envoyez une requête PUT à cette route avec un JSON contenant l'identifiant du badge.
    """
    
    if request.method == 'PUT':
        badge = request.get_json()
        badge_id = badge.get('badge_id')
        
        api_url = f"{server_back_end_url}/api/scanne/badge"
        try:
            response = requests.put(api_url, json=badge_id)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Erreur de requête vers l'URL distante 1: {str(e)}"
            return jsonify({
                "status": 500, 
                "error": error_message
            }), 500
    response = {
        "status": 405,
        "error": "Vous devez utiliser une requête PUT pour cette route."
    }
    return jsonify(response), 405 

@app.route('/api/send/request/open/door', methods=['PUT'])
@login_required
def sendRequestOpenDoor():
    
    if request.method == 'PUT':
        write_log("FRONT : Envoi de la demande.")
        
        data  = request.get_json()

        api_url = f"{server_door_url}/door/publish"
        try:
            response = requests.put(api_url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            write_log(f"Erreur de requête vers l'URL distante : {str(e)}")
            error_message = f"Erreur de requête vers l'URL distante : {str(e)}"
            return jsonify({
                "status": 500, 
                "error": error_message
            }), 200
    response = {
        "status": 405,
        "error": "Vous devez utiliser une requête PUT pour cette route."
    }
    return jsonify(response), 200 

#
#
#   Admin Pannel
#
#

@app.route('/api/admin/get/all-users', methods=['GET'])
@login_required
@roles_required([2])
def getAdminAllUsers():
    """
        Récupère toutes les informations des utilisateurs avec le rôle 1 pour le panneau d'administration.

        Cette route permet à un administrateur authentifié d'obtenir les informations de tous les utilisateurs ayant le rôle 1
        pour le panneau d'administration. Les informations sont obtenues en effectuant une requête GET vers un serveur distant.

        Args:
            Aucun argument n'est requis dans la fonction.

        Returns:
            - Si la requête GET réussit et retourne un code de statut 200, la fonction renvoie les informations des utilisateurs sous
            forme de JSON.
            - Si une erreur se produit lors de la requête vers le serveur distant, la fonction renvoie un message d'erreur JSON approprié
            avec un code de statut 500.
            - Si l'utilisateur n'est pas un administrateur (rôle 2), la fonction renvoie un message d'erreur JSON avec un code de statut 403.
            - Si la méthode HTTP n'est pas GET, la fonction renvoie un message d'erreur JSON avec un code de statut 405.

        Raises:
            Aucune exception n'est levée dans cette fonction.

        Exemple d'utilisation:
            Un administrateur peut accéder à cette route en effectuant une requête GET. Si la requête réussit, il recevra les informations
            des utilisateurs avec le rôle 1 pour le panneau d'administration.
    """

    if request.method == 'GET':
        api_url = f"{server_back_end_url}/api/admin/get/all-users"
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Erreur de requête vers l'URL distante : {str(e)}"
            return jsonify({
                "status": 500, 
                "error": error_message
            }), 500
    response = {
        "status": 405,
        "error": "Vous devez utiliser une requête GET pour cette route."
    }
    return jsonify(response), 405 

@app.route('/api/admin/delete/account', methods=['POST'])
@login_required
@roles_required([2])
def adminDeleteAccount():
    """
        Supprime un compte utilisateur en tant qu'administrateur.

        Cette route permet à un administrateur authentifié de supprimer un compte utilisateur en effectuant une requête POST vers
        un serveur distant.

        Args:
            Aucun argument n'est requis dans la fonction. Les données du compte utilisateur à supprimer sont envoyées via une requête JSON.

        Returns:
            - Si la requête POST réussit et retourne un code de statut 200, la fonction renvoie les données de réponse JSON du serveur distant,
            y compris le message "Utilisateur supprimé".
            - Si une erreur se produit lors de la requête vers le serveur distant, la fonction renvoie un message d'erreur JSON approprié
            avec un code de statut 500.
            - Si l'utilisateur n'est pas un administrateur (rôle 2), la fonction renvoie un message d'erreur JSON avec un code de statut 403.
            - Si la méthode HTTP n'est pas POST, la fonction renvoie un message d'erreur JSON avec un code de statut 405.

        Raises:
            Aucune exception n'est levée dans cette fonction.

        Exemple d'utilisation:
            Un administrateur peut accéder à cette route en effectuant une requête POST avec les données du compte utilisateur à supprimer.
            Si la requête réussit, le compte utilisateur est supprimé, et la réponse JSON contient le message "Utilisateur supprimé".
    """

    if request.method == 'POST':
        data = request.get_json()
        user_id = data['user_id']
        print(user_id)
        
        api_url = f"{server_back_end_url}/api/delete/account"
        try:
            response = requests.post(api_url, json={'user_id': user_id})
            response.raise_for_status()
            if(response.status_code  == 200):
                response_data = response.json()
                response_data['message'] = 'Utilisateur supprimé.'
                return response_data
            
        except requests.exceptions.RequestException as e:
            flash(f"Erreur de requête vers l'URL distante 1: {str(e)}", 'error')  
            return redirect(url_for('settings'))
            
    flash('Vous devez utiliser une requête POST', 'error')  
    return redirect(url_for('settings'))
