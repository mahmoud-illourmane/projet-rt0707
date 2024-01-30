from app import app

from flask import render_template, request, abort, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from functools import wraps

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
#   Configuration of LoginManager
#
#

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

@app.route('/custom_403_error_page')
def custom_403_error_page():
    return render_template('errors/403_error.html'), 403

@login_manager.user_loader
def load_user(user_id):
    """
        Charge un utilisateur à partir de l'identifiant utilisateur.

        Cette fonction est utilisée par Flask-Login pour retrouver un utilisateur en fonction de son ID stocké dans la session.

        Args:
            user_id (str): L'identifiant de l'utilisateur à charger.

        Returns:
            - Si un utilisateur correspondant à l'identifiant est trouvé dans la session et le chargement réussit, la fonction renvoie une
            instance de la classe User avec les données de l'utilisateur.
            - Si aucun utilisateur correspondant n'est trouvé, la fonction renvoie None pour indiquer qu'aucun utilisateur n'est trouvé.

        Raises:
            Aucune exception n'est levée dans cette fonction.

        Exemple d'utilisation:
            Cette fonction est utilisée automatiquement par Flask-Login lorsque vous appelez `login_user(user)` pour charger un utilisateur
            dans la session.
    """
    
    user_session = session.get('user_session')
    if user_session and user_id == user_session.get('id'):
        return User(user_id, user_session.get('first_name'), user_session.get('email'), user_session.get('role'))
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """
        Gère les tentatives d'accès non autorisées à une page protégée par l'authentification.

        Cette fonction est utilisée par Flask-Login pour rediriger automatiquement les utilisateurs non authentifiés vers la page
        de connexion (ou une autre page définie) lorsqu'ils tentent d'accéder à une page protégée.

        Returns:
            - Une redirection vers la page de connexion (ou une autre page définie) avec un message d'erreur approprié.

        Raises:
            Aucune exception n'est levée dans cette fonction.

        Exemple d'utilisation:
            Cette fonction est utilisée automatiquement par Flask-Login lorsque vous décorez une route avec `@login_required`.
    """
    
    flash("Veuillez vous connecter pour accéder à cette page.", "error")
    return redirect(url_for('login'))
    
#
#
#   Authentification
#
#

@app.route('/sign-up', methods=['GET'])
def signUp():
    """
        Affiche la page de création de compte (sign-up).

        Cette route permet aux utilisateurs d'accéder à la page de création de compte en effectuant une requête GET.
        Si une autre méthode HTTP est utilisée, un message d'erreur est affiché et l'utilisateur est redirigé vers la page de création de compte.

        Returns:
            - Un rendu du modèle HTML de la page de création de compte (signUp.html) lorsqu'une requête GET est reçue.
            - Une redirection vers la page de création de compte avec un message d'erreur lorsqu'une autre méthode HTTP est utilisée.

        Raises:
            Aucune exception n'est levée dans cette fonction.

        Exemple d'utilisation:
            Cette route permet aux utilisateurs d'accéder à la page de création de compte en effectuant une requête GET.
    """
    
    if request.method == 'GET':
        return render_template('views/signIn-signUp/signUp.html')
    
    flash('Vous devez utiliser une requête GET', 'danger')  
    return redirect(url_for('signUp'))
    
@app.route('/log-in', methods=['GET'])
def login():
    """
        Gère l'affichage de la page de connexion (log-in).

        Cette route permet aux utilisateurs de se connecter en affichant la page de connexion (log-in) lorsqu'une requête GET est reçue.
        Si un utilisateur est déjà authentifié, il est redirigé en fonction de son rôle.
        Si une autre méthode HTTP est utilisée, un message d'erreur est affiché et l'utilisateur est redirigé vers la page de connexion.

        Returns:
            - Une redirection vers la page d'accueil ('index') si un utilisateur authentifié a le rôle 1.
            - Une redirection vers le tableau de bord de l'administrateur ('admin_dashboard') si un utilisateur authentifié a le rôle 2.
            - Un rendu du modèle HTML de la page de connexion (logIn.html) si une requête GET est reçue et aucun utilisateur n'est authentifié.
            - Une redirection vers la page de connexion avec un message d'erreur si une autre méthode HTTP est utilisée.

        Raises:
            Aucune exception n'est levée dans cette fonction.

        Exemple d'utilisation:
            Cette route permet aux utilisateurs de se connecter en affichant la page de connexion (log-in) lorsqu'une requête GET est reçue.
    """
    
    if request.method == 'GET':
        if current_user.is_authenticated:
            if int(current_user.role) == 1:
                return redirect(url_for('index'))
            elif int(current_user.role) == 2:
                return redirect(url_for('admin_dashboard'))
        else:
            return render_template('views/signIn-signUp/signIn.html')
    else:
        flash("Vous devez utiliser la méthode GET pour cette route.", "error")
        return redirect(url_for('login'))
    
@app.route('/logout')
@login_required
def logout():
    """
        Gère la déconnexion de l'utilisateur.

        Cette route permet à l'utilisateur authentifié de se déconnecter en utilisant la fonction 'logout_user()' du module Flask-Login.
        Après la déconnexion, un message de confirmation est affiché et l'utilisateur est redirigé vers la page de connexion ('login').

        Returns:
            - Une redirection vers la page de connexion ('login') après la déconnexion de l'utilisateur.
            - Un message de confirmation ("Au revoir !") est affiché lors de la déconnexion.

        Raises:
            Aucune exception n'est levée dans cette fonction.

        Exemple d'utilisation:
            Cette route permet à un utilisateur authentifié de se déconnecter en accédant à la page '/logout'.
    """
    
    logout_user()
    flash("Au revoir !")
    return redirect(url_for('login'))

#
#
# Admin Application
#
#

@app.route('/admin-index', methods=['GET'])
@login_required
@roles_required([2])
def admin_dashboard():
    """
        Affiche le tableau de bord de l'administrateur.

        Cette route permet d'afficher le tableau de bord de l'administrateur lorsqu'il est connecté et possède le rôle 2.
        L'accès à cette page est réservé aux administrateurs.

        Returns:
            - Une vue HTML du tableau de bord de l'administrateur.

        Raises:
            Aucune exception n'est levée dans cette fonction.
    """
    
    return render_template('views/admin/admin-index.html')

@app.route('/admin/gestion/users', methods=['GET'])
@login_required
@roles_required([2])
def adminGestionsUsers():
    """
        Affiche la gestion des utilisateurs pour l'administrateur.

        Cette route permet à l'administrateur d'accéder à la gestion des utilisateurs lorsqu'il est connecté et possède le rôle 2.
        L'accès à cette page est réservé aux administrateurs.

        Returns:
            - Une vue HTML de la gestion des utilisateurs pour l'administrateur.

        Raises:
            Aucune exception n'est levée dans cette fonction.
    """
    
    if request.method == 'GET':
        return render_template('views/admin/admin-users.html')
    return render_template('errors/405_error.html'), 405

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
@roles_required([1, 2])
def index():
    if request.method == 'GET':
        return render_template('views/index.html')
    return render_template('errors/405_error.html'), 405

@app.route('/gestion/ticket', methods=['GET'])
@login_required
def gestionTicket():
    if request.method == 'GET':
        return render_template('views/interfaces/gestion-ticket.html')
    return render_template('errors/405_error.html'), 405

@app.route('/settings', methods=['GET'])
@login_required
def settings():
    if request.method == 'GET':
        return render_template('views/setting/setting.html')
    return render_template('errors/405_error.html'), 405

#
# Authentification not required
#

@app.route('/achat/ticket', methods=['GET'])
def achatTicket():
    if request.method == 'GET':
        return render_template('views/interfaces/achat-ticket.html')
    return render_template('errors/405_error.html'), 405
    
#
# IOT Simulation
#

@app.route('/scanner/porte', methods=['GET'])
def scannerPorte():
    if request.method == 'GET':
        return render_template('views/interfaces/scan-porte.html')
    return render_template('errors/405_error.html'), 405
