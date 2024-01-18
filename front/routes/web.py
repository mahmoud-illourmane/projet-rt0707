from app import app
from datetime import datetime
import requests
from flask import render_template, request, abort, redirect, url_for, flash, session

from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user
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

#
#
#   Web Application 
#
#

@app.route('/', methods=['GET'])
# @login_required
def index():
    if request.method == 'GET':
        return render_template('web/index.html')
    abort(405)

@app.route('/scanner/porte', methods=['GET'])
# @login_required
def scannerPorte():
    if request.method == 'GET':
        return render_template('web/scan-porte.html')
    abort(405)

@app.route('/achat/ticket', methods=['GET'])
# @login_required
def achatTicket():
    if request.method == 'GET':
        return render_template('web/achat-ticket.html')
    abort(405)

@app.route('/gestion/ticket', methods=['GET'])
# @login_required
def gestionTicket():
    if request.method == 'GET':
        return render_template('web/gestion-ticket.html')
    abort(405) 
    
    
    
    
    
# Initialisation de LoginManager
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

#
#
#   Authentification
#
#

# Rechargement de l'utilisateur
# @login_manager.user_loader
# def load_user(user_id):
#     user_info = session.get('user_info')
#     if user_info and user_id == user_info.get('id'):
#         return User(user_id, user_info.get('first_name'), user_info.get('email'))
#     return None

# @app.route('/signUp', methods=['GET', 'POST'])
# def signUp():
#     """
#     Summary:
#         Cette route renvoie une vue HTML permettant de s'inscrire.
#         Elle gère également le processus d'inscription.

#     Returns:
#             str: Une vue HTML.
#     """
    
#     if request.method == 'GET':
#         return render_template('signIn-signUp/sigUp.html')
    
#     elif request.method == 'POST':
#         firstName = request.form['firstName']
#         email = request.form['email']
#         password = request.form['password']
#         passwordConfirm = request.form['passwordConfirm']
        
#         # Vérifie si les mots de passe correspondent
#         if password != passwordConfirm:
#             flash('Les mots de passe ne correspondent pas. Veuillez réessayer.')
#             return redirect(url_for('signUp')) 
        
#         # Je forge les données de la requête pour le fichier api.py du serveur front 
#         # Ce n'est pas idéal..
#         data = {
#             "firstName": firstName,
#             "email": email,
#             "password": password
#         }
#         # Convertir le dictionnaire en une chaîne JSON
#         user_data = json.dumps(data)
#         # Spécification de l'en-tête "Content-Type" pour indiquer que j'envoie du JSON
#         headers = {'Content-Type': 'application/json'}
#         api_url = f"{server_front_end_url}/api/signUp"
        
#         try:
#             response = requests.post(api_url, data=user_data, headers=headers)
#             response.raise_for_status()
            
#             if response.status_code == 201:
#                 response_data = response.json()
#                 user = User(response_data.get('id'), response_data.get('first_name'), response_data.get('email'))
#                 login_user(user)
#                 # Stocker les informations dans la session
#                 session['user_info'] = {'id': user.id, 'first_name': user.first_name, 'email': user.email}
#                 return redirect(url_for('index'))
#             elif response.status_code == 409:
#                 flash("L'email est déjà utilisé.")
#                 return redirect(url_for('signUp')) 
#             else:
#                 flash("Une erreur s'est produite web.py.")
#                 return redirect(url_for('signUp')) 
#         except requests.exceptions.RequestException as e:
#             error_message = f"Erreur de requête vers l'URL distante : {str(e)}"
#             flash(error_message)
#             return redirect(url_for('signUp')) 
#     abort(405)
    
# @app.route('/logIn', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # Ici, envoie la requête à l'API du serveur back-end
#         email = request.form['email']
#         password = request.form['password']
        
#         headers = {'Content-Type': 'application/json'}
#         api_url = f"{server_front_end_url}/api/logIn"
#         response = requests.post(api_url, json={'email': email, 'password': password}, headers=headers)

#         if response.status_code == 200:
#             response_data = response.json()
#             user = User(response_data.get('id'), response_data.get('first_name'), response_data.get('email'))
#             login_user(user)
#             # Stocker les informations dans la session
#             session['user_info'] = {'id': user.id, 'first_name': user.first_name, 'email': user.email}
#             return redirect(url_for('index'))
#         flash('L\'email ou le mot de passe est incorrect.', 'error')
#         return redirect(url_for('login'))

#     return render_template('signIn-signUp/login.html')

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash("Au revoir !")
#     return redirect(url_for('login'))

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
 
# @login_manager.unauthorized_handler
# def unauthorized():
#     flash("Veuillez vous connecter pour accéder à cette page.", "error")
#     return redirect(url_for('login'))
    
