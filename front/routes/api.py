from app import app
from flask import request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

import json
import requests

from src.classes.user import User

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
            
# Initialisation de LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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
                    
                    flash('Bienvenue', 'success')  
                    return redirect(url_for('index'))
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

@app.route('/api/get/generals-infos-user', methods=['GET'])
@login_required
def getGeneralsInfosUser():
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
    if request.method == 'GET':
        # Si l'utilisateur est authentifier on envoi son id
        if current_user.is_authenticated:
            user_id = str(current_user.id)
        else:
            response = {
                "status": 403,
                "error": "Vous devez être authentifié."
            }
            return jsonify(response), 403 
    
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

@app.route('/api/scanne/ticket', methods=['PUT'])
def scanneTicket():
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

@app.route('/api/purchase', methods=['POST'])
def purchase():
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
#
#   Settings View
#
#
#

@app.route('/api/settings', methods=['PUT'])
@login_required
def updateDataSettings():
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
                flash('Votre compte à bien été supprimé', 'error')  
                return redirect(url_for('signUp'))
            
            flash('Une erreur s\'est produite pendant la suppression.', 'error')  
            return redirect(url_for('settings'))
        except requests.exceptions.RequestException as e:
            flash(f"Erreur de requête vers l'URL distante 1: {str(e)}", 'error')  
            return redirect(url_for('settings'))
            
    flash('Vous devez utiliser une requête POST', 'error')  
    return redirect(url_for('settings'))

