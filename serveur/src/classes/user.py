from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from pymongo.errors import PyMongoError
import datetime

from src.classes.mongoDb import MongoDBManager
from src.classes.qrCode import QRCode

class User:
    def __init__(self, db_manager: MongoDBManager, firstName, email, password, role, id=None):
        """
        Initialise un nouvel user ou charge un user existant.

        :param db_manager: Instance de MongoDBManager pour interagir avec la base de données.
        :param firstName: firstName de l'user.
        :param email: Email de l'user.
        :param password: Mot de passe de l'user (non hashé pour un nouveau, hashé pour un existant).
        :param role: Rôle de l'user.
        :param id: ID de l'user dans la base de données (pour un user existant).
        """
        
        self.db_manager = db_manager
        self.id = id
        self.firstName = firstName
        self.email = email
        self.password = password
        self.role = role
    
    def createUser(self):
        """
            Crée un nouvel utilisateur dans la base de données.
        """
        
        try:
            # Vérification de si l'email existe déjà
            users_collection = self.db_manager.get_collection('users')
            if users_collection.find_one({'email': self.email}):
                return jsonify({
                    'status': 400,
                    'error': 'Email déjà utilisé'
                }), 400

            if self.role not in [1, 2, 3]:
                return jsonify({
                    'status': 400,
                    'error': 'La valeur du rôle n\'est pas reconnue.'
                }), 400

            # Hacher le mot de passe avant de l'insérer
            hashed_password = generate_password_hash(self.password)

            # Créer le document utilisateur
            user_data = {
                'firstName': self.firstName,
                'email': self.email,
                'password': hashed_password,
                'role': self.role
            }

            # Insérer l'utilisateur dans la base de données
            result = users_collection.insert_one(user_data)
            if result.inserted_id:
                return jsonify({
                    'status': 201,
                    'id': str(result.inserted_id),
                    'role': self.role
                }), 201
            else:
                return jsonify({
                    'status': 304, 
                    'error': 'Une erreur lors de l\'insertion'
                }), 304

        except PyMongoError as e:
            return jsonify({
                'status': 500,
                'error': f"Une erreur PyMongo s'est produite : {str(e)}"
            }), 500
        except Exception as e:
            return jsonify({
                'status': 500,
                'error': f"Une erreur inattendue s'est produite : {str(e)}"
            }), 500
        
    def updateUser(self):
        """
        Met à jour un user existant dans la base de données.
        """
        if self.id:
            self.db_manager.get_users().update_one(
                {"_id": ObjectId(self.id)},
                {"$set": {
                    "firstName": self.firstName,
                    "email": self.email,
                    "password": self.password,  # Assurer que le mot de passe est déjà hashé.
                    "role": self.role
                }}
            )

    def deleteUser(self):
        """
        Supprime l'user de la base de données.
        """
        if self.id:
            self.db_manager.get_users().delete_one({"_id": ObjectId(self.id)})

    def to_json(self):
        """
        Retourne la représentation JSON de l'user.
        """
        return {
            "_id": str(self.id),
            "firstName": self.firstName,
            "email": self.email,
            "password": self.password,  # Le mot de passe doit être hashé.
            "role": self.role
        }

    @staticmethod
    def getGeneralsInfosUser(db_manager, user_id):
        """
            Récupère des informations générales sur un utilisateur, notamment le nombre de tickets achetés ce mois-ci
            et le QR Code du dernier ticket acheté.

            Args:
                db_manager (MongoDBManager): Le gestionnaire de base de données MongoDB.
                user_id (str): L'identifiant de l'utilisateur pour lequel récupérer les informations.

            Returns:
                tuple: Un tuple contenant un objet JSON et un code HTTP.

                Le JSON contient les informations suivantes :
                - 'status' (int): Le code de statut de la réponse.
                - 'ticket_count' (int): Le nombre de tickets achetés ce mois-ci par l'utilisateur.
                - 'last_ticket_qrcode' (dict): Les informations du dernier ticket acheté sous forme de QR Code en Base64.
                
                Le code HTTP indique le succès ou l'échec de la requête.
        """

        try:
            tickets_collection = db_manager.get_collection('tickets')
        except PyMongoError as e:
            return jsonify({
                'status': 500,
                'error': f"Une erreur PyMongo s'est produite : {str(e)}"
            }), 500

        # Obtenir la date de début du mois actuel en UTC
        today_utc = datetime.datetime.utcnow()
        first_day_of_month_utc = today_utc.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        try:
            # Compter les tickets de l'utilisateur achetés ce mois-ci
            ticket_count = tickets_collection.count_documents({
                'user_id': user_id,
                'date_achat': {'$gte': first_day_of_month_utc}
            })

            # Récupérer le dernier ticket acheté
            last_ticket = tickets_collection.find_one(
                {'user_id': user_id},
                sort=[('date_achat', -1)]
            )
            if last_ticket:
                id = str(last_ticket.get('_id', 'N/A'))
                date_achat = last_ticket.get('date_achat', 'N/A')
                type = last_ticket.get('type', 'N/A')
                validite = last_ticket.get('validite', 'N/A')
                etat = last_ticket.get('etat', 'N/A')
                nb_scannes = last_ticket.get('nb_scannes', '0')
                
                last_ticket_qrcode = QRCode.create_qr_code_with_info(id, date_achat, type, validite, etat, nb_scannes)
            else:
                last_ticket_qrcode = None
                
            return jsonify({
                'status': 200,
                'ticket_count': ticket_count,
                'last_ticket_qrcode': last_ticket_qrcode
            }), 200
        except PyMongoError as e:
            return jsonify({
                'status': 500,
                'error': f"Une erreur PyMongo s'est produite : {str(e)}"
            }), 500
         
    @staticmethod
    def login(db_manager, email:str, password:str):
        """
            Authentifie un utilisateur en vérifiant l'email et le mot de passe dans la base de données.

            :param db_manager: Instance de MongoDBManager pour interagir avec la base de données.
            :param email: Adresse e-mail de l'utilisateur à authentifier.
            :param password: Mot de passe de l'utilisateur à vérifier.
            :return: Une réponse JSON avec le statut HTTP approprié.
        """

        user = db_manager.get_collection('users').find_one({"email": email})
        if user:
            # Vérification du mot de passe haché
            if check_password_hash(user['password'], password):
                return jsonify({
                    'status': 200,
                    'id': str(user['_id']),
                    'first_name': user['firstName'],
                    'email': user['email'],
                    'role': user['role']
                }), 200
        return jsonify({
            'status': 401,
        }), 401
