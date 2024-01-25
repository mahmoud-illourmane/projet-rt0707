from app import app
from datetime import datetime
import requests
from flask import render_template, request, abort, redirect, url_for, flash, session

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

import json

from src.classes.user import User  

# Accède à la variable globale depuis la configuration Flask
server_front_end_url = app.config['SERVER_FRONT_END_URL']

"""
|   This file contains all the routes for the frontend of this application.
|
|   Author: Mahmoud ILLOURMANE
|   Date: January 18, 2024
"""

# Initialisation de LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#
#
#   Authentification
#
#

# Rechargement de l'utilisateur
@login_manager.user_loader
def load_user(user_id):
    user_session = session.get('user_session')
    if user_session and user_id == user_session.get('id'):
        return User(user_id, user_session.get('first_name'), user_session.get('email'), user_session.get('role'))
    return None

@login_manager.unauthorized_handler
def unauthorized():
    flash("Veuillez vous connecter pour accéder à cette page.", "error")
    return redirect(url_for('login'))
    
@app.route('/sign-up', methods=['GET'])
def signUp():
    """
    Summary:
        Cette route renvoie une vue HTML permettant de s'inscrire.
        Elle gère également le processus d'inscription.

    Returns:
            str: Une vue HTML.
    """
    
    if request.method == 'GET':
        return render_template('views/signIn-signUp/signUp.html')
    
    flash('Vous devez utiliser une requête GET', 'danger')  
    return redirect(url_for('signUp'))
    
@app.route('/log-in', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('views/signIn-signUp/signIn.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Au revoir !")
    return redirect(url_for('login'))

# @app.route('/deleteUser', methods=['POST'])
# def deleteUser_():
#     """_summary_
#     Cette méthode se charge de supprimer un utilisateur
    
#     Returns:
#         _type_: une réponse Json
#     """
    
#     if request.method == 'POST':
        
#         if current_user.is_authenticated:
#             user_id = current_user.id

#         headers = {'Content-Type': 'application/json'}
#         api_url = f"{server_front_end_url}/api/deleteUser"
        
#         try:
#             response = requests.post(api_url, json={"user_id": user_id}, headers=headers)
#             response.raise_for_status()
#             if response.status_code == 204:
#                 logout_user()
#                 flash("Votre compte a bien été supprimé")
#                 return redirect(url_for('login'))
            
#             flash("Une erreur s'est produite pendant la suppression.")
#             return redirect(url_for('/'))
#         except requests.exceptions.RequestException as e:
#             error_message = f"Erreur de requête vers l'URL distante 78: {str(e)}"
#             flash(error_message)
#             return redirect(url_for('signUp')) 
 

    
#
#
#   Web Application 
#
#

#
# Authentification required
#

@app.route('/', methods=['GET'])
@login_required
def index():
    if request.method == 'GET':
        return render_template('views/index.html')
    abort(405)

@app.route('/gestion/ticket', methods=['GET'])
@login_required
def gestionTicket():
    if request.method == 'GET':
        return render_template('views/interfaces/gestion-ticket.html')
    abort(405) 

#
# Authentification not required
#

@app.route('/achat/ticket', methods=['GET'])
def achatTicket():
    if request.method == 'GET':
        return render_template('views/interfaces/achat-ticket.html')
    abort(405)
    
#
# IOT Simulation
#

@app.route('/scanner/porte', methods=['GET'])
def scannerPorte():
    if request.method == 'GET':
        return render_template('views/interfaces/scan-porte.html')
    abort(405)